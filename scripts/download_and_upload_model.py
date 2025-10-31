import os
import argparse
from huggingface_hub import snapshot_download
import subprocess

def run(cmd):
    """Ejecuta un comando en shell y muestra su salida"""
    print(">", " ".join(cmd))
    subprocess.check_call(cmd)

def main():
    p = argparse.ArgumentParser(description="Descarga un modelo de Hugging Face y súbelo a un bucket de GCP.")
    p.add_argument("--model", default="tabularisai/multilingual-sentiment-analysis", help="Nombre del modelo en Hugging Face")
    p.add_argument("--out", default="./models/multilingual-sentiment", help="Ruta local donde guardar el modelo descargado")
    p.add_argument("--bucket", default="model-senti-analy-ia", help="Nombre del bucket en GCP")
    p.add_argument("--hf_token", default=None, help="Token de Hugging Face (si el modelo fuera privado)")
    p.add_argument("--compress", action="store_true", help="Comprimir el modelo antes de subirlo")
    args = p.parse_args()

    # Crear carpeta de salida
    os.makedirs(args.out, exist_ok=True)

    print(f"📦 Descargando modelo '{args.model}' en '{args.out}' ...")
    snapshot_download(
        repo_id=args.model,
        local_dir=args.out,
        local_dir_use_symlinks=False,
        token=args.hf_token
    )
    print("✅ Descarga completada.")

    # Comprimir si se indicó
    if args.compress:
        tarfile = args.out.rstrip("/") + ".tar.gz"
        print(f"🗜️  Comprimiendo en {tarfile} ...")
        run(["tar", "-czf", tarfile, "-C", os.path.dirname(args.out), os.path.basename(args.out)])
        print(f"☁️  Subiendo archivo comprimido al bucket gs://{args.bucket}/ ...")
        run(["gsutil", "-m", "cp", tarfile, f"gs://{args.bucket}/"])
    else:
        print(f"☁️  Subiendo carpeta del modelo al bucket gs://{args.bucket}/models/ ...")
        run(["gsutil", "-m", "cp", "-r", args.out, f"gs://{args.bucket}/models/"])

    print("🎯 Proceso completado con éxito.")

if __name__ == "__main__":
    main()
