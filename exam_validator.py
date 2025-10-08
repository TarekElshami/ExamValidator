import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import zipfile
import os
from pathlib import Path
import tempfile
import shutil


class ExamValidator:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador de Exámenes ExamWatcher")
        self.root.geometry("900x700")

        self.zip_path = None
        self.reference_folder = None
        self.temp_dir = None

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title = ttk.Label(main_frame, text="Validador de Exámenes ExamWatcher",
                          font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=3, pady=10)

        ttk.Label(main_frame, text="1. Seleccionar ZIP del examen:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.zip_label = ttk.Label(main_frame, text="Ningún archivo seleccionado", foreground="gray")
        self.zip_label.grid(row=1, column=1, sticky=tk.W, padx=5)
        ttk.Button(main_frame, text="Examinar...", command=self.select_zip).grid(row=1, column=2, padx=5)

        ttk.Label(main_frame, text="2. Carpeta de referencia (inicial):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ref_label = ttk.Label(main_frame, text="Opcional - Para comparar snapshot", foreground="gray")
        self.ref_label.grid(row=2, column=1, sticky=tk.W, padx=5)
        ttk.Button(main_frame, text="Examinar...", command=self.select_reference).grid(row=2, column=2, padx=5)

        self.validate_btn = ttk.Button(main_frame, text="VALIDAR EXAMEN",
                                       command=self.validate_exam, state=tk.DISABLED)
        self.validate_btn.grid(row=3, column=0, columnspan=3, pady=20)

        ttk.Label(main_frame, text="Resultados de Validación:",
                  font=('Arial', 12, 'bold')).grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=5)

        self.results_text = scrolledtext.ScrolledText(main_frame, width=100, height=30,
                                                      font=('Courier', 9))
        self.results_text.grid(row=5, column=0, columnspan=3, pady=5)

        self.results_text.tag_config("error", foreground="red", font=('Courier', 9, 'bold'))
        self.results_text.tag_config("warning", foreground="#FF4500", font=('Courier', 9, 'bold'))
        self.results_text.tag_config("success", foreground="green", font=('Courier', 9, 'bold'))
        self.results_text.tag_config("info", foreground="blue", font=('Courier', 9, 'bold'))
        self.results_text.tag_config("header", font=('Courier', 10, 'bold'))

    def select_zip(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar ZIP del examen",
            filetypes=[("Archivos ZIP", "*.zip"), ("Todos los archivos", "*.*")]
        )
        if filename:
            self.zip_path = filename
            self.zip_label.config(text=os.path.basename(filename), foreground="black")
            self.validate_btn.config(state=tk.NORMAL)

    def select_reference(self):
        dirname = filedialog.askdirectory(title="Seleccionar carpeta de referencia")
        if dirname:
            self.reference_folder = dirname
            self.ref_label.config(text=os.path.basename(dirname), foreground="black")

    def calculate_file_hash(self, content):
        """Calcula el hash de un archivo individual (para backups)"""
        hash_value = 29366927
        if isinstance(content, str):
            content = content.encode('utf-8')

        for i, byte in enumerate(content):
            mult = 1 if (i % 2) == 0 else 100
            signed_byte = byte if byte < 128 else byte - 256
            hash_value += signed_byte * mult

        return hash_value

    def calculate_resume_hash(self, zip_path, student_name, log_messages):
        """Calcula el hash de resume.txt EXACTAMENTE como Java - SIN EXCLUIR NINGÚN ARCHIVO"""
        hash_value = 29366927

        # 1. Hash del nombre del estudiante
        name_bytes = student_name.encode('utf-8')
        for i, byte in enumerate(name_bytes):
            mult = 1 if (i % 2) == 0 else 100
            signed_byte = byte if byte < 128 else byte - 256
            hash_value += signed_byte * mult

        # 2. Hash de TODOS los archivos en el ZIP (excepto resume.txt que se añade al final)
        processed_files = []

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Obtener todos los archivos y ordenarlos alfabéticamente
            all_files = sorted([f for f in zip_ref.infolist() if not f.is_dir()],
                               key=lambda x: x.filename)

            for file_info in all_files:
                file_name = file_info.filename

                # Solo excluir resume.txt (se procesa al final en Java)
                if file_name.endswith('resume.txt'):
                    continue

                processed_files.append(file_name)
                position = 0

                with zip_ref.open(file_name) as f:
                    while True:
                        buffer = f.read(4096)
                        if not buffer:
                            break
                        for i, byte in enumerate(buffer):
                            global_pos = position + i
                            mult = 1 if (global_pos % 2) == 0 else 100
                            signed_byte = byte if byte < 128 else byte - 256
                            hash_value += signed_byte * mult
                        position += len(buffer)

        # DEBUG
        print(f"\n=== CÁLCULO DE HASH ===")
        print(f"Hash después del nombre: {hash_value}")
        print(f"Archivos procesados: {len(processed_files)}")
        for f in processed_files[:20]:
            print(f"  - {f}")
        if len(processed_files) > 20:
            print(f"  ... y {len(processed_files) - 20} más")

        # 3. Agregar el número de mensajes de log
        hash_value += len(log_messages)
        print(f"Mensajes de log: {len(log_messages)}")
        print(f"Hash final: {hash_value}")

        return hash_value

    def parse_resume(self, content):
        lines = content.split('\n')
        student_name = lines[0].strip() if lines else ""
        num_files = 0
        declared_hash = 0
        log_messages = []
        in_log_section = False

        for line in lines:
            if 'Num files:' in line:
                try:
                    num_files = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'Hash Value:' in line:
                try:
                    declared_hash = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'Log messages:' in line:
                in_log_section = True
            elif in_log_section and line.strip() and 'Hash Value:' not in line:
                log_messages.append(line.strip())

        return {
            'student_name': student_name,
            'num_files': num_files,
            'declared_hash': declared_hash,
            'log_messages': log_messages
        }

    def extract_initial_snapshot(self, log_messages, project_folder):
        snapshot = {}
        in_snapshot = False

        for msg in log_messages:
            if '=== Initial folder snapshot:' in msg:
                in_snapshot = True
                continue
            if '=== End of snapshot ===' in msg:
                break

            if in_snapshot and msg.startswith('File:'):
                parts = msg.split('|')
                if len(parts) >= 3:
                    file_path = parts[0].replace('File:', '').strip()
                    try:
                        size = int(parts[1].split(':')[1].strip().replace('bytes', '').strip())
                        lines = int(parts[2].split(':')[1].strip())

                        file_path = os.path.normpath(file_path)
                        project_folder = os.path.normpath(project_folder)
                        if file_path.startswith(project_folder):
                            rel_path = os.path.relpath(file_path, project_folder)
                            snapshot[rel_path] = {
                                'size': size,
                                'lines': lines,
                                'path': file_path
                            }
                    except:
                        pass

        return snapshot

    def extract_backup_hashes(self, log_messages):
        backup_files = {}
        for msg in log_messages:
            if 'FILE COPIED:' in msg and 'Hash:' in msg and 'Backup:' in msg:
                try:
                    hash_part = msg.split('Hash:')[1].split('|')[0].strip()
                    expected_hash = int(hash_part)
                    backup_part = msg.split('Backup:')[1].strip()
                    file_name = os.path.basename(backup_part)
                    backup_files[file_name] = expected_hash
                except:
                    pass
        return backup_files

    def count_suspicious_lines(self, log_messages):
        """Cuenta líneas modificadas con internet activo, excluyendo cambios de 0 líneas y archivos de backup"""
        total_lines = 0
        suspicious_events = []

        for msg in log_messages:
            if '[SUSPICIOUS: network was active]' in msg:
                # Excluir archivos de backup (.copywatcher_backup)
                if '.copywatcher_backup' in msg:
                    continue

                if 'MODIFIED:' in msg:
                    if 'lines:' in msg:
                        try:
                            lines_part = msg.split('lines:')[1].split(']')[0]
                            if '[' in lines_part:
                                change = lines_part.split('[')[0].strip()
                                change_value = int(change.replace('+', '').replace('-', ''))

                                # Solo contar si hay cambio real
                                if change_value != 0:
                                    total_lines += abs(change_value)
                                    suspicious_events.append(msg)
                        except:
                            pass

                elif 'NEW FILE:' in msg:
                    try:
                        if 'lines)' in msg:
                            lines_part = msg.split('lines)')[0].split(',')[-1].strip()
                            lines_count = int(lines_part.split()[0])

                            if lines_count > 0:
                                total_lines += lines_count
                                suspicious_events.append(msg)
                    except:
                        pass

        return total_lines, suspicious_events

    def compare_with_reference(self, snapshot, reference_folder):
        differences = []
        reference_files = {}
        for root, dirs, files in os.walk(reference_folder):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, reference_folder)
                try:
                    actual_size = os.path.getsize(file_path)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        actual_lines = len(f.readlines())
                    reference_files[os.path.normpath(rel_path)] = {
                        'size': actual_size,
                        'lines': actual_lines
                    }
                except:
                    pass

        for rel_path, expected in snapshot.items():
            if rel_path in reference_files:
                actual = reference_files[rel_path]
                if actual['size'] != expected['size'] or actual['lines'] != expected['lines']:
                    differences.append({
                        'file': rel_path,
                        'expected_size': expected['size'],
                        'actual_size': actual['size'],
                        'expected_lines': expected['lines'],
                        'actual_lines': actual['lines']
                    })
            else:
                differences.append({
                    'file': rel_path,
                    'expected_size': expected['size'],
                    'actual_size': 'N/A',
                    'expected_lines': expected['lines'],
                    'actual_lines': 'N/A'
                })

        return differences

    def validate_backup_files(self, backup_folder, expected_hashes):
        results = []
        for file_name, expected_hash in expected_hashes.items():
            file_path = os.path.join(backup_folder, file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    calculated_hash = self.calculate_file_hash(content)
                    matches = calculated_hash == expected_hash
                    results.append({
                        'file': file_name,
                        'expected': expected_hash,
                        'calculated': calculated_hash,
                        'matches': matches
                    })
                except Exception as e:
                    results.append({
                        'file': file_name,
                        'error': str(e)
                    })
            else:
                results.append({
                    'file': file_name,
                    'error': 'Archivo no encontrado en backup'
                })
        return results

    def find_backup_folder(self, root_dir):
        for root, dirs, files in os.walk(root_dir):
            if '.copywatcher_backup' in dirs:
                return os.path.join(root, '.copywatcher_backup')
        return None

    def validate_exam(self):
        self.results_text.delete(1.0, tk.END)
        if not self.zip_path:
            messagebox.showerror("Error", "Debe seleccionar un archivo ZIP")
            return

        try:
            self.temp_dir = tempfile.mkdtemp()
            self.log("Extrayendo archivo ZIP...\n", "info")
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)

            resume_path = None
            project_folder = None
            for root, dirs, files in os.walk(self.temp_dir):
                if 'resume.txt' in files:
                    resume_path = os.path.join(root, 'resume.txt')
                    project_folder = os.path.dirname(resume_path)
                    break

            if not resume_path:
                self.log("ERROR: No se encontró resume.txt en el ZIP\n", "error")
                return

            with open(resume_path, 'r', encoding='utf-8') as f:
                resume_content = f.read()

            parsed = self.parse_resume(resume_content)

            self.log("=" * 80 + "\n", "header")
            self.log("INFORMACIÓN DEL ESTUDIANTE\n", "header")
            self.log("=" * 80 + "\n", "header")
            self.log(f"Nombre: {parsed['student_name']}\n", "info")

            start_time = None
            for msg in parsed['log_messages']:
                if 'Project folder selected:' in msg:
                    start_time = msg.split(' - ')[0]
                    break
            if start_time:
                self.log(f"Hora de inicio: {start_time}\n\n", "info")

            self.log("=" * 80 + "\n", "header")
            self.log("1. VALIDACIÓN DE HASH DEL RESUME.TXT\n", "header")
            self.log("=" * 80 + "\n", "header")

            calculated_hash = self.calculate_resume_hash(self.zip_path, parsed['student_name'], parsed['log_messages'])
            hash_matches = calculated_hash == parsed['declared_hash']
            if hash_matches:
                self.log(f"✓ Hash correcto\n", "success")
                self.log(f"  Hash declarado: {parsed['declared_hash']}\n")
                self.log(f"  Hash calculado: {calculated_hash}\n\n")
            else:
                self.log(f"✗ HASH INCORRECTO - POSIBLE MANIPULACIÓN\n", "error")
                self.log(f"  Hash declarado: {parsed['declared_hash']}\n", "error")
                self.log(f"  Hash calculado: {calculated_hash}\n\n", "error")
                self.log(f"  Diferencia: {abs(calculated_hash - parsed['declared_hash'])}\n", "error")

            self.log("=" * 80 + "\n", "header")
            self.log("2. COMPARACIÓN DE SNAPSHOT INICIAL\n", "header")
            self.log("=" * 80 + "\n", "header")

            snapshot = self.extract_initial_snapshot(parsed['log_messages'], project_folder)
            self.log(f"Archivos en snapshot inicial: {len(snapshot)}\n")

            if self.reference_folder:
                self.log("\nComparando con carpeta de referencia...\n", "info")
                differences = self.compare_with_reference(snapshot, self.reference_folder)
                if differences:
                    self.log(f"✗ Se encontraron {len(differences)} diferencias:\n", "warning")
                    for diff in differences:
                        self.log(f"\n  Archivo: {diff['file']}\n", "warning")
                        self.log(f"    Tamaño esperado: {diff['expected_size']}, actual: {diff['actual_size']}\n")
                        self.log(f"    Líneas esperadas: {diff['expected_lines']}, actuales: {diff['actual_lines']}\n")
                else:
                    self.log("✓ El snapshot coincide con la carpeta de referencia\n", "success")
            else:
                self.log("⚠ No se proporcionó carpeta de referencia para comparar\n\n", "warning")

            self.log("\n" + "=" * 80 + "\n", "header")
            self.log("3. VALIDACIÓN DE ARCHIVOS DE BACKUP\n", "header")
            self.log("=" * 80 + "\n", "header")

            backup_folder = self.find_backup_folder(self.temp_dir)
            backup_hashes = self.extract_backup_hashes(parsed['log_messages'])
            self.log(f"Archivos esperados en backup: {len(backup_hashes)}\n")

            if backup_folder:
                validation_results = self.validate_backup_files(backup_folder, backup_hashes)
                failed = [r for r in validation_results if not r.get('matches', False)]
                if failed:
                    self.log(f"\n✗ {len(failed)} archivos con problemas:\n", "error")
                    for result in failed:
                        if 'error' in result:
                            self.log(f"\n  {result['file']}: {result['error']}\n", "error")
                        else:
                            self.log(f"\n  {result['file']}:\n", "error")
                            self.log(f"    Hash esperado: {result['expected']}\n")
                            self.log(f"    Hash calculado: {result['calculated']}\n")
                else:
                    self.log("✓ Todos los hashes de backup son correctos\n", "success")
            else:
                self.log("✗ No se encontró la carpeta .copywatcher_backup\n\n", "error")

            self.log("\n" + "=" * 80 + "\n", "header")
            self.log("4. ACTIVIDAD SOSPECHOSA (INTERNET ACTIVO)\n", "header")
            self.log("=" * 80 + "\n", "header")

            suspicious_lines, suspicious_events = self.count_suspicious_lines(parsed['log_messages'])
            self.log(f"Total de líneas cambiadas con internet activo: {suspicious_lines}\n")

            if suspicious_lines > 10:
                self.log(f"✗ LÍMITE EXCEDIDO (máximo: 10 líneas)\n", "error")
                self.log(f"\nEventos sospechosos detectados: {len(suspicious_events)}\n", "warning")
                if suspicious_events:
                    self.log("\nEventos sospechosos:\n", "warning")
                    for event in suspicious_events:
                        self.log(f"  - {event}\n", "warning")
            else:
                self.log(f"✓ Dentro del límite permitido (10 líneas)\n", "success")

            self.log("\n" + "=" * 80 + "\n", "header")
            self.log("RESUMEN FINAL\n", "header")
            self.log("=" * 80 + "\n", "header")

            all_ok = hash_matches and suspicious_lines <= 10
            if all_ok:
                self.log("✓ EXAMEN VÁLIDO - Sin problemas críticos detectados\n", "success")
            else:
                self.log("✗ EXAMEN CON PROBLEMAS - Revisar errores arriba\n", "error")

        except Exception as e:
            self.log(f"\nERROR GENERAL: {str(e)}\n", "error")
            import traceback
            self.log(traceback.format_exc(), "error")
        finally:
            if self.temp_dir and os.path.exists(self.temp_dir):
                try:
                    shutil.rmtree(self.temp_dir)
                except:
                    pass

    def log(self, message, tag=None):
        if tag:
            self.results_text.insert(tk.END, message, tag)
        else:
            self.results_text.insert(tk.END, message)
        self.results_text.see(tk.END)
        self.root.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExamValidator(root)
    root.mainloop()