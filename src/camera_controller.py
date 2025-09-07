import os
import re
import shlex
import time
import subprocess
from typing import List, Dict, Optional, Tuple

class GPhoto2:
    ENV = {"LANG": "C", "LC_ALL": "C"}  # salidas estables para parseo

    # ---------- Helpers de proceso ----------
    @staticmethod
    def _run(args: List[str], *, timeout: Optional[float] = None,
             capture_output: bool = True, check: bool = False) -> subprocess.CompletedProcess:
        # Ejecuta 'gphoto2' con args como lista (sin shell), respetando locale estable
        return subprocess.run(
            ["gphoto2"] + args,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            check=check,
            env={**os.environ, **GPhoto2.ENV}
        )

    @staticmethod
    def _run_cmdline(cmdline: str, *, timeout: Optional[float] = None,
                     capture_output: bool = True, check: bool = False) -> subprocess.CompletedProcess:
        # Igual que _run, pero aceptando string (usa shlex.split para espacios seguros)
        args = shlex.split(cmdline)
        return GPhoto2._run(args, timeout=timeout, capture_output=capture_output, check=check)

    # ---------- Gestión de procesos que estorban ----------
    @staticmethod
    def kill_initial_process() -> bool:
        try:
            for proc in ("gvfsd-gphoto2", "gphoto2", "gvfs-mtp-volume-monitor"):
                subprocess.run(["killall", "-q", proc], check=False)
            return True
        except Exception:
            return False

    # ---------- Descubrimiento de cámaras ----------
    @staticmethod
    def get_cameras() -> Dict[str, str]:
        """
        Devuelve dict {modelo_o_modelo(n): puerto}, p.ej. {"Sony ILCE-6400": "usb:002,006", "Sony ILCE-6400(1)": "usb:004,003"}
        """
        try:
            cp = GPhoto2._run(["--auto-detect"], timeout=10, capture_output=True, check=False)
            lines = cp.stdout.strip().splitlines()
            cams: Dict[str, str] = {}

            # Saltar encabezados, parsear con regex robusta (modelo + >=2 espacios + puerto)
            rx = re.compile(r"^(?P<model>.+?)\s{2,}(?P<port>(usb:\d{3},\d+|ptpip:.*|serial:.*))$")
            for line in lines[2:]:
                line = line.strip()
                if not line:
                    continue
                m = rx.match(line)
                if not m:
                    continue
                model = m.group("model").strip()
                port = m.group("port").strip()

                # desambiguar nombres duplicados
                base = model
                idx = 0
                while model in cams:
                    idx += 1
                    model = f"{base}({idx})"
                cams[model] = port

            return cams or {None: None}
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve cameras: {e}")

    @staticmethod
    def get_serial_for_port(camera_port: str, timeout: float = 8.0) -> Optional[str]:
        """
        Lee el serial mediante --summary (línea 'Serial Number').
        """
        try:
            cp = GPhoto2._run(["--port", camera_port, "--summary"], timeout=timeout, capture_output=True, check=False)
            if cp.returncode != 0:
                return None
            m = re.search(r"Serial Number\s*:\s*(.+)", cp.stdout)
            return m.group(1).strip() if m else None
        except Exception:
            return None

    @staticmethod
    def get_speed_for_port(camera_port: str) -> Optional[str]:
        """
        Intenta detectar 12M/480M consultando 'lsusb -t' y mapeando el Bus/Device del puerto.
        (Best effort; puede devolver None si no se logra mapear.)
        """
        try:
            # puerto usb:BBB,DDD
            m = re.match(r"usb:(\d{3}),(\d+)$", camera_port)
            if not m:
                return None
            bus, dev = m.group(1), m.group(2)

            # Buscar en lsusb -t una línea con 'Bus BBB' no existe directo; se mapea por topología.
            # Best effort: devolver la primera velocidad listada.
            out = subprocess.run(["lsusb", "-t"], capture_output=True, text=True).stdout
            ms = re.findall(r"(\d+)(?:-[-\d\.]+)?\s+:\s+.*?(\d+M)", out)  # pares (bus?, velocidad)
            # Simple: si hay 480M en la salida, asumimos High-Speed disponible.
            return "480M" if "480M" in out else ("12M" if "12M" in out else None)
        except Exception:
            return None

    # ---------- Config ----------
    @staticmethod
    def get_config(camera_port: Optional[str], camera_config: str) -> Dict[str, str]:
        if not camera_port:
            return {}
        cp = GPhoto2._run(["--port", camera_port, "--get-config", camera_config],
                          timeout=10, capture_output=True, check=False)
        if cp.returncode != 0:
            raise RuntimeError(cp.stderr.strip() or "get-config failed")
        configs: Dict[str, str] = {}
        for line in cp.stdout.splitlines():
            line = line.strip()
            if line.startswith("Choice:"):
                # "Choice: 0 Auto" → idx, valor
                parts = line.split(" ", 2)
                if len(parts) == 3:
                    idx = parts[1].strip()
                    val = parts[2].strip()
                    configs[val] = idx
        return configs

    @staticmethod
    def set_config(camera_port: str, camera_config: str, config_value: str) -> bool:
        try:
            cp = GPhoto2._run(["--port", camera_port, "--set-config", f"{camera_config}={config_value}"],
                              timeout=15, capture_output=True, check=False)
            return cp.returncode == 0
        except Exception:
            return False

    # ---------- Captura ----------
    @staticmethod
    def _ping(camera_port: str, timeout: float = 8.0) -> None:
        try:
            GPhoto2._run(["--port", camera_port, "--summary"], timeout=timeout, capture_output=True, check=False)
        except Exception:
            pass  # best effort

    @staticmethod
    def capture_image(camera_port: str, download_path: str, file_name: str) -> bool:
        os.makedirs(download_path, exist_ok=True)
        file_path = os.path.join(download_path, file_name)

        print(f"[GPhoto2] Preparando captura en {camera_port} → {file_path}")
        GPhoto2._ping(camera_port)

        # Retries con backoff
        for attempt in range(1, 4):
            try:
                print(f"[GPhoto2] Intento {attempt}/3")
                cp = GPhoto2._run(
                    ["--port", camera_port, "--capture-image-and-download", "--filename", file_path],
                    timeout=40, capture_output=True, check=False
                )
                if cp.returncode == 0 and os.path.exists(file_path):
                    time.sleep(0.2)
                    return True
                else:
                    err = (cp.stderr or "").strip()
                    out = (cp.stdout or "").strip()
                    print(f"[GPhoto2] Falló intento {attempt}: {err or out}")
            except subprocess.TimeoutExpired:
                print(f"[GPhoto2] Timeout en intento {attempt}")
            time.sleep(0.7 * attempt)  # backoff
        return False

    # ---------- Utilidades de alto nivel ----------
    @staticmethod
    def inventory() -> List[Tuple[str, str, Optional[str], Optional[str]]]:
        """
        Devuelve lista de (modelo, puerto, serial, velocidad_aprox).
        """
        cams = GPhoto2.get_cameras()
        inv = []
        for model, port in cams.items():
            if not model or not port:
                continue
            serial = GPhoto2.get_serial_for_port(port)
            speed = GPhoto2.get_speed_for_port(port)
            inv.append((model, port, serial, speed))
        return inv
