import os
import sys
import urllib.request
import zipfile
import subprocess

def download_file(url, dest):
    print(f"[*] Descargando: {url}")
    print(f"[*] Guardando en: {dest}")
    # Descargar con cabecera de User-Agent para evitar bloqueos
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
        out_file.write(response.read())

def extract_zip(zip_path, extract_to):
    print(f"[*] Extrayendo: {zip_path} en {extract_to}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def main():
    print("=" * 60)
    print("    INSTALACIÓN AUTOMÁTICA DE ENTORNOS PORTABLES DE BAJO NIVEL")
    print("=" * 60)
    
    bin_dir = r"C:\Users\Pc\Documents\GitHub\lenguaje y compiladores\bin"
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
        
    # 1. Node.js Portable
    node_exe = os.path.join(bin_dir, "node-v20.11.1-win-x64", "node.exe")
    if not os.path.exists(node_exe):
        node_url = "https://nodejs.org/dist/v20.11.1/node-v20.11.1-win-x64.zip"
        node_zip = os.path.join(bin_dir, "node.zip")
        try:
            download_file(node_url, node_zip)
            extract_zip(node_zip, bin_dir)
            os.remove(node_zip)
            print("[+] Node.js portátil configurado con éxito.")
        except Exception as e:
            print(f"[-] Error al descargar/extraer Node.js: {e}")
    else:
        print("[+] Node.js ya está disponible localmente.")

    # 2. Zig Portable
    zig_exe = os.path.join(bin_dir, "zig-windows-x86_64-0.11.0", "zig.exe")
    if not os.path.exists(zig_exe):
        zig_url = "https://ziglang.org/download/0.11.0/zig-windows-x86_64-0.11.0.zip"
        zig_zip = os.path.join(bin_dir, "zig.zip")
        try:
            download_file(zig_url, zig_zip)
            extract_zip(zig_zip, bin_dir)
            os.remove(zig_zip)
            print("[+] Zig portátil configurado con éxito.")
        except Exception as e:
            print(f"[-] Error al descargar/extraer Zig: {e}")
    else:
        print("[+] Zig ya está disponible localmente.")

    # 3. Rust (to user cargo bin)
    rustc_exe = os.path.expandvars(r"%USERPROFILE%\.cargo\bin\rustc.exe")
    if not os.path.exists(rustc_exe):
        rustup_url = "https://win.rustup.rs/x86_64"
        rustup_exe = os.path.join(bin_dir, "rustup-init.exe")
        try:
            download_file(rustup_url, rustup_exe)
            print("[*] Instalando Rust y Cargo de forma silenciosa (puede tardar de 1 a 2 minutos)...")
            # Ejecutar de forma no interactiva con -y
            subprocess.run([rustup_exe, "-y", "--default-toolchain", "stable"], check=True)
            if os.path.exists(rustup_exe):
                os.remove(rustup_exe)
            print("[+] Rust e infraestructura de compilación listos.")
        except Exception as e:
            print(f"[-] Error al instalar Rust: {e}")
    else:
        print("[+] Rust ya está instalado y disponible en el perfil de usuario.")
        
    print("=" * 60)
    print("          INSTALACIÓN DE ENTORNOS COMPLETADA CON ÉXITO        ")
    print("=" * 60)

if __name__ == "__main__":
    main()
