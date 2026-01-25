import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import zipfile
import os
import tempfile
import shutil
import json
import traceback


# --- LocalizationManager (Clase para gestionar las cadenas de texto) ---

class LocalizationManager:
    """Clase para cargar y gestionar las cadenas de texto localizadas."""

    def __init__(self, default_lang='es'):
        self.language = default_lang
        self.strings = {}
        # Cargar idiomas al inicializar
        self.load_language('es', 'strings_es.json')
        self.load_language('en', 'strings_en.json')
        # Establecer idioma inicial
        self.set_language(default_lang)

    def load_language(self, lang_code, filename):
        """Carga las cadenas de texto desde un archivo JSON."""
        try:
            if not os.path.exists(filename):
                self._create_dummy_file(lang_code, filename)

            with open(filename, 'r', encoding='utf-8') as f:
                self.strings[lang_code] = json.load(f)
        except Exception as e:
            print(f"Error al cargar el idioma {lang_code} desde {filename}: {e}")
            self.strings[lang_code] = {}

    def _create_dummy_file(self, lang_code, filename):
        """Crea archivos dummy para pruebas si no existen, incluyendo los nuevos textos."""
        if lang_code == 'es':
            data = {
                "window_title": "ExamWatcher Log Visualizer",
                "menu_file": "Archivo",
                "menu_file_zip": "Seleccionar ZIP del examen...",
                "menu_file_ref": "Seleccionar Carpeta de Referencia...",
                "menu_file_exit": "Salir",
                "menu_lang": "Idioma",
                "menu_lang_es": "Español",
                "menu_lang_en": "Inglés",
                "title": "Validador de Exámenes ExamWatcher",
                "step1": "1. Seleccionar ZIP del examen:",
                "step2": "2. Carpeta de referencia (inicial):",
                "zip_none": "Ningún archivo seleccionado",
                "ref_none": "Opcional - Para comparar snapshot",
                "button_browse": "Examinar...",
                "button_validate": "VALIDAR EXAMEN",
                "results_title": "Resultados de Validación:",
                "error_zip_select": "Debe seleccionar un archivo ZIP",
                "log_extracting": "Extrayendo archivo ZIP...",
                "log_error_resume": "ERROR: No se encontró resume.txt en el ZIP",
                "log_info_header": "=" * 80 + "\nINFORMACIÓN DEL ESTUDIANTE\n" + "=" * 80 + "\n",
                "log_name": "Nombre: {}",
                "log_start_time": "Hora de inicio: {}\n\n",
                "log_hash_header": "=" * 80 + "\n1. VALIDACIÓN DE HASH DEL RESUME.TXT\n" + "=" * 80 + "\n",
                "log_hash_ok": "✓ Hash correcto\n",
                "log_hash_declared": "  Hash declarado: {}",
                "log_hash_calculated": "  Hash calculado: {}",
                "log_hash_error": "✗ HASH INCORRECTO - POSIBLE MANIPULACIÓN\n",
                "log_hash_diff": "  Diferencia: {}",
                "log_snapshot_header": "=" * 80 + "\n2. COMPARACIÓN DE SNAPSHOT INICIAL\n" + "=" * 80 + "\n",
                "log_snapshot_files": "Archivos en snapshot inicial: {}",
                "log_comparing_ref": "\nComparando con carpeta de referencia...",
                "log_diff_count_error": "✗ Se encontraron {} diferencias:",
                "log_diff_file": "\n  Archivo: {}",
                "log_diff_size": "    Tamaño esperado: {}, actual: {}",
                "log_diff_lines": "    Líneas esperadas: {}, actuales: {}",
                "log_snapshot_ok": "✓ El snapshot coincide con la carpeta de referencia\n",
                "log_no_ref": "⚠ No se proporcionó carpeta de referencia para comparar\n\n",
                "log_backup_header": "\n" + "=" * 80 + "\n3. VALIDACIÓN DE ARCHIVOS DE BACKUP\n" + "=" * 80 + "\n",
                "log_backup_expected": "Archivos esperados en backup: {}",
                "log_backup_found_none": "No se esperaban copias de seguridad y no se encontraron. Comportamiento normal.\n",
                "log_backup_count_error": "\n✗ {} archivos con problemas:",
                "log_backup_file_error": "\n  {}: {}",
                "log_backup_hash_error": "\n  {}:\n    Hash esperado: {}\n    Hash calculado: {}",
                "log_backup_ok": "✓ Todos los hashes de backup son correctos\n",
                "log_backup_folder_error": "✗ No se encontró la carpeta .copywatcher_backup\n\n",
                "log_suspicious_header": "\n" + "=" * 80 + "\n4. ACTIVIDAD SOSPECHOSA (INTERNET ACTIVO)\n" + "=" * 80 + "\n",
                "log_suspicious_lines": "Total de líneas cambiadas con internet activo: {}",
                "log_suspicious_limit_error": "✗ LÍMITE EXCEDIDO (máximo: 10 líneas)",
                "log_suspicious_events_count": "\nEventos sospechosos detectados: {}",
                "log_suspicious_event": "\nEventos sospechosos:\n",
                "log_suspicious_event_item": "  - {}",
                "log_suspicious_ok": "✓ Dentro del límite permitido (10 líneas)\n",
                "log_network_header": "\n" + "=" * 80 + "\n5. DETECCIÓN DE CONEXIÓN (EVENTOS DE RED)\n" + "=" * 80 + "\n",
                "log_network_count": "⚠ Se detectaron {} eventos de conexión a internet:",
                "log_network_item": "  - {}",
                "log_network_ok": "✓ No se detectaron eventos de conexión a internet\n",
                # NUEVOS TEXTOS
                "log_unauthorized_app_header": "\n" + "=" * 80 + "\n6. APLICACIONES NO AUTORIZADAS DETECTADAS\n" + "=" * 80 + "\n",
                "log_unauthorized_app_count": "⚠ {} aplicación(es) no autorizada(s) detectada(s):",
                "log_unauthorized_app_item": "  - {}",
                "log_unauthorized_app_ok": "✓ No se detectaron aplicaciones no autorizadas\n",
                # FIN NUEVOS TEXTOS
                "log_summary_header": "\n" + "=" * 80 + "\nRESUMEN FINAL\n" + "=" * 80 + "\n",
                "log_summary_ok": "✓ EXAMEN VÁLIDO - Sin problemas críticos detectados\n",
                "log_summary_warning": "⚠ EXAMEN VÁLIDO CON ADVERTENCIAS - Se detectaron archivos de backup (Revisar)\n",
                "log_summary_error": "✗ EXAMEN CON PROBLEMAS - Revisar errores arriba\n",
                "log_general_error": "\nERROR GENERAL: {}\n"
            }
        elif lang_code == 'en':
            data = {
                "window_title": "ExamWatcher Log Visualizer",
                "menu_file": "File",
                "menu_file_zip": "Select Exam ZIP...",
                "menu_file_ref": "Select Reference Folder...",
                "menu_file_exit": "Exit",
                "menu_lang": "Language",
                "menu_lang_es": "Spanish",
                "menu_lang_en": "English",
                "title": "ExamWatcher Exam Validator",
                "step1": "1. Select Exam ZIP:",
                "step2": "2. Reference Folder (Initial):",
                "zip_none": "No file selected",
                "ref_none": "Optional - For snapshot comparison",
                "button_browse": "Browse...",
                "button_validate": "VALIDATE EXAM",
                "results_title": "Validation Results:",
                "error_zip_select": "You must select a ZIP file",
                "log_extracting": "Extracting ZIP file...",
                "log_error_resume": "ERROR: resume.txt not found in ZIP",
                "log_info_header": "=" * 80 + "\nSTUDENT INFORMATION\n" + "=" * 80 + "\n",
                "log_name": "Name: {}",
                "log_start_time": "Start Time: {}\n\n",
                "log_hash_header": "=" * 80 + "\n1. RESUME.TXT HASH VALIDATION\n" + "=" * 80 + "\n",
                "log_hash_ok": "✓ Correct Hash\n",
                "log_hash_declared": "  Declared Hash: {}",
                "log_hash_calculated": "  Calculated Hash: {}",
                "log_hash_error": "✗ INCORRECT HASH - POSSIBLE MANIPULATION\n",
                "log_hash_diff": "  Difference: {}",
                "log_snapshot_header": "=" * 80 + "\n2. INITIAL SNAPSHOT COMPARISON\n" + "=" * 80 + "\n",
                "log_snapshot_files": "Files in initial snapshot: {}",
                "log_comparing_ref": "\nComparing with reference folder...",
                "log_diff_count_error": "✗ Found {} differences:",
                "log_diff_file": "\n  File: {}",
                "log_diff_size": "    Expected size: {}, actual: {}",
                "log_diff_lines": "    Expected lines: {}, actual: {}",
                "log_snapshot_ok": "✓ Snapshot matches reference folder\n",
                "log_no_ref": "⚠ No reference folder provided for comparison\n\n",
                "log_backup_header": "\n" + "=" * 80 + "\n3. BACKUP FILE VALIDATION\n" + "=" * 80 + "\n",
                "log_backup_expected": "Expected backup files: {}",
                "log_backup_found_none": "No backups were expected and none were found. Normal behavior.\n",
                "log_backup_count_error": "\n✗ {} files with issues:",
                "log_backup_file_error": "\n  {}: {}",
                "log_backup_hash_error": "\n  {}:\n    Expected Hash: {}\n    Calculated Hash: {}",
                "log_backup_ok": "✓ All backup hashes are correct\n",
                "log_backup_folder_error": "✗ .copywatcher_backup folder not found\n\n",
                "log_suspicious_header": "\n" + "=" * 80 + "\n4. SUSPICIOUS ACTIVITY (NETWORK ACTIVE)\n" + "=" * 80 + "\n",
                "log_suspicious_lines": "Total lines changed with active network: {}",
                "log_suspicious_limit_error": "✗ LIMIT EXCEEDED (max: 10 lines)",
                "log_suspicious_events_count": "\nDetected suspicious events: {}",
                "log_suspicious_event": "\nSuspicious events:\n",
                "log_suspicious_event_item": "  - {}",
                "log_suspicious_ok": "✓ Within allowed limit (10 lines)\n",
                "log_network_header": "\n" + "=" * 80 + "\n5. CONNECTION DETECTION (NETWORK EVENTS)\n" + "=" * 80 + "\n",
                "log_network_count": "⚠ Detected {} internet connection events:",
                "log_network_item": "  - {}",
                "log_network_ok": "✓ No internet connection events detected\n",
                # NUEVOS TEXTOS
                "log_unauthorized_app_header": "\n" + "=" * 80 + "\n6. UNAUTHORIZED APPLICATIONS DETECTED\n" + "=" * 80 + "\n",
                "log_unauthorized_app_count": "⚠ {} unauthorized application(s) detected:",
                "log_unauthorized_app_item": "  - {}",
                "log_unauthorized_app_ok": "✓ No unauthorized applications detected\n",
                # FIN NUEVOS TEXTOS
                "log_summary_header": "\n" + "=" * 80 + "\nFINAL SUMMARY\n" + "=" * 80 + "\n",
                "log_summary_ok": "✓ VALID EXAM - No critical issues detected\n",
                "log_summary_warning": "⚠ VALID EXAM WITH WARNINGS - Backup files detected (Review)\n",
                "log_summary_error": "✗ EXAM WITH ISSUES - Review errors above\n",
                "log_general_error": "\nGENERAL ERROR: {}\n"
            }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def set_language(self, lang_code):
        """Cambia el idioma activo."""
        if lang_code in self.strings:
            self.language = lang_code
            return True
        return False

    def get_string(self, key, *args):
        """Obtiene la cadena de texto para una clave dada, aplicando formato si hay argumentos."""
        s = self.strings.get(self.language, {}).get(key, f"MISSING_STRING:{key}")
        if s.startswith("MISSING_STRING"):
            s = self.strings.get('es', {}).get(key, f"MISSING_STRING:{key}")
        try:
            return s.format(*args)
        except IndexError:
            return s


# --- CLASE PRINCIPAL: ExamValidator (Con UX Mejorado) ---

class ExamValidator:
    def __init__(self, root):
        self.root = root
        self.lang_manager = LocalizationManager()

        self.root.geometry("1000x800")
        self.root.minsize(800, 600)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.zip_path = None
        self.reference_folder = None
        self.temp_dir = None

        self.setup_menu()
        self.setup_ui()
        self.update_ui_text()

    def setup_menu(self):
        """Crea la barra de menú."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(menu=file_menu, label=self.lang_manager.get_string("menu_file"))
        file_menu.add_command(label=self.lang_manager.get_string("menu_file_zip"), command=self.select_zip)
        file_menu.add_command(label=self.lang_manager.get_string("menu_file_ref"), command=self.select_reference)
        file_menu.add_separator()
        file_menu.add_command(label=self.lang_manager.get_string("menu_file_exit"), command=self.root.quit)

        lang_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(menu=lang_menu, label=self.lang_manager.get_string("menu_lang"))
        lang_menu.add_command(label=self.lang_manager.get_string("menu_lang_es"),
                              command=lambda: self.set_language('es'))
        lang_menu.add_command(label=self.lang_manager.get_string("menu_lang_en"),
                              command=lambda: self.set_language('en'))

        self.menubar = menubar

    def set_language(self, lang_code):
        """Cambia el idioma y actualiza la UI."""
        if self.lang_manager.set_language(lang_code):
            self.update_ui_text()
            self.setup_menu()

    def update_ui_text(self):
        """Actualiza todos los textos estáticos de la UI."""
        self.root.title(self.lang_manager.get_string("window_title"))
        self.title_label.config(text=self.lang_manager.get_string("title"))
        self.label_step1.config(text=self.lang_manager.get_string("step1"))
        self.label_step2.config(text=self.lang_manager.get_string("step2"))

        if not self.zip_path:
            self.zip_label.config(text=self.lang_manager.get_string("zip_none"))
        if not self.reference_folder:
            self.ref_label.config(text=self.lang_manager.get_string("ref_none"))

        self.btn_zip.config(text=self.lang_manager.get_string("button_browse"))
        self.btn_ref.config(text=self.lang_manager.get_string("button_browse"))
        self.validate_btn.config(text=self.lang_manager.get_string("button_validate"))
        self.label_results.config(text=self.lang_manager.get_string("results_title"))

    def setup_ui(self):
        """Configura la interfaz principal con adaptabilidad y prioridad en el área del log."""

        main_frame = ttk.Frame(self.root, padding="20 10 20 10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        main_frame.grid_columnconfigure(1, weight=1)  # Columna del path label se expande
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(2, weight=0)

        main_frame.grid_rowconfigure(6, weight=1)  # Fila del log (ScrolledText) se expande

        # Título
        self.title_label = ttk.Label(main_frame, text="", font=('Arial', 18, 'bold'), anchor='center')
        self.title_label.grid(row=0, column=0, columnspan=3, pady="10 15", sticky=(tk.W, tk.E))

        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E),
                                                             pady="0 10")

        # 1. Seleccionar ZIP
        self.label_step1 = ttk.Label(main_frame, text="", font=('Arial', 10, 'bold'))
        self.label_step1.grid(row=2, column=0, sticky=tk.W, pady=5, padx="0 10")

        self.zip_label = ttk.Label(main_frame, text="", foreground="gray", anchor=tk.W, relief=tk.GROOVE,
                                   padding="5 3")
        self.zip_label.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)

        self.btn_zip = ttk.Button(main_frame, text="Examinar...", command=self.select_zip)
        self.btn_zip.grid(row=2, column=2, padx="10 0")

        # 2. Carpeta de referencia
        self.label_step2 = ttk.Label(main_frame, text="", font=('Arial', 10, 'bold'))
        self.label_step2.grid(row=3, column=0, sticky=tk.W, pady=5, padx="0 10")

        self.ref_label = ttk.Label(main_frame, text="", foreground="gray", anchor=tk.W, relief=tk.GROOVE,
                                   padding="5 3")
        self.ref_label.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5)

        self.btn_ref = ttk.Button(main_frame, text="Examinar...", command=self.select_reference)
        self.btn_ref.grid(row=3, column=2, padx="10 0")

        # Botón de validación
        self.validate_btn = ttk.Button(main_frame, text="",
                                       command=self.validate_exam, state=tk.DISABLED,
                                       style='Accent.TButton')
        self.validate_btn.grid(row=4, column=0, columnspan=3, pady="20 15",
                               sticky=(tk.W, tk.E))

        # Resultados Título
        self.label_results = ttk.Label(main_frame, text="", font=('Arial', 12, 'bold'))
        self.label_results.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady="15 5")

        # Área de Visualización del Log (ScrolledText)
        self.results_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD,
                                                      font=('Courier', 10), relief=tk.SUNKEN)
        self.results_text.grid(row=6, column=0, columnspan=3, pady="5 0",
                               sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configuración de Tags
        self.results_text.tag_config("error", foreground="red", font=('Courier', 10, 'bold'))
        self.results_text.tag_config("warning", foreground="#FF4500", font=('Courier', 10, 'bold'))
        self.results_text.tag_config("success", foreground="green", font=('Courier', 10, 'bold'))
        self.results_text.tag_config("info", foreground="blue", font=('Courier', 10, 'normal'))
        self.results_text.tag_config("header", font=('Courier', 11, 'bold'))

        try:
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('Accent.TButton', font=('Arial', 12, 'bold'), background='#0078D4', foreground='black')
        except Exception:
            pass

    def select_zip(self):
        filename = filedialog.askopenfilename(
            title=self.lang_manager.get_string("menu_file_zip"),
            filetypes=[("Archivos ZIP", "*.zip"), ("Todos los archivos", "*.*")]
        )
        if filename:
            self.zip_path = filename
            display_text = os.path.basename(filename)
            self.zip_label.config(text=display_text, foreground="black")
            self.validate_btn.config(state=tk.NORMAL)

    def select_reference(self):
        dirname = filedialog.askdirectory(title=self.lang_manager.get_string("menu_file_ref"))
        if dirname:
            self.reference_folder = dirname
            display_text = os.path.basename(dirname)
            self.ref_label.config(text=display_text, foreground="black")

    # Métodos de cálculo de hash y parsing (lógica de negocio)
    def calculate_file_hash(self, content):
        hash_value = 29366927
        if isinstance(content, str):
            content = content.encode('utf-8')

        for i, byte in enumerate(content):
            mult = 1 if (i % 2) == 0 else 100
            signed_byte = byte if byte < 128 else byte - 256
            hash_value += signed_byte * mult

        return hash_value

    def calculate_resume_hash(self, zip_path, student_name, log_messages):
        hash_value = 29366927
        name_bytes = student_name.encode('utf-8')
        for i, byte in enumerate(name_bytes):
            mult = 1 if (i % 2) == 0 else 100
            signed_byte = byte if byte < 128 else byte - 256
            hash_value += signed_byte * mult

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            all_files = sorted([f for f in zip_ref.infolist() if not f.is_dir()],
                               key=lambda x: x.filename)
            for file_info in all_files:
                file_name = file_info.filename
                if file_name.endswith('resume.txt'):
                    continue
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
        hash_value += len(log_messages)
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

    def analyze_log_activity(self, log_messages):
        """
        Analiza el log en busca de:
        1. Líneas de código cambiadas con red activa (sospechoso).
        2. Eventos de conexión a internet (aunque no haya cambios).
        3. Aplicaciones no autorizadas detectadas.
        """
        total_suspicious_lines = 0
        suspicious_events = []
        network_events = []
        unauthorized_app_events = []

        for msg in log_messages:
            # --- 1. Actividad Sospechosa (Red Activa + Cambios) ---
            if '[SUSPICIOUS: network was active]' in msg:
                # Ignorar eventos de backup
                if '.copywatcher_backup' in msg:
                    continue

                if 'MODIFIED:' in msg:
                    if 'lines:' in msg:
                        try:
                            lines_part = msg.split('lines:')[1].split(']')[0]
                            if '[' in lines_part:
                                change = lines_part.split('[')[0].strip()
                                change_value = int(change.replace('+', '').replace('-', ''))
                                if change_value != 0:
                                    total_suspicious_lines += abs(change_value)
                                    suspicious_events.append(msg)
                        except:
                            pass

                elif 'NEW FILE:' in msg:
                    try:
                        if 'lines)' in msg:
                            lines_part = msg.split('lines)')[0].split(',')[-1].strip()
                            lines_count = int(lines_part.split()[0])
                            if lines_count > 0:
                                total_suspicious_lines += lines_count
                                suspicious_events.append(msg)
                    except:
                        pass

            # --- 2. Detección de conexión aunque no haya cambiado nada ---
            if "Network connection detected" in msg or "Conexión a red detectada" in msg or "Conexion a red detectada" in msg:
                network_events.append(msg)

            # --- 3. Aplicaciones no autorizadas ---
            # Patrón: "2025/10/26 00:03:29 - Detectado Chrome - Cierre el programa"
            if ' - Detectado ' in msg and ' - Cierre el programa' in msg:
                unauthorized_app_events.append(msg)
            # Versión en inglés por si acaso
            if ' - Detected ' in msg and ' - Close the program' in msg:
                unauthorized_app_events.append(msg)

        return total_suspicious_lines, suspicious_events, network_events, unauthorized_app_events

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

    # --- MÉTODO PRINCIPAL DE VALIDACIÓN ---
    def validate_exam(self):
        self.results_text.delete(1.0, tk.END)
        if not self.zip_path:
            messagebox.showerror(self.lang_manager.get_string("window_title"),
                                 self.lang_manager.get_string("error_zip_select"))
            return

        critical_error = False

        try:
            self.temp_dir = tempfile.mkdtemp()
            self.log(self.lang_manager.get_string("log_extracting") + "\n", "info")
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
                self.log(self.lang_manager.get_string("log_error_resume") + "\n", "error")
                critical_error = True
                return

            with open(resume_path, 'r', encoding='utf-8') as f:
                resume_content = f.read()

            parsed = self.parse_resume(resume_content)

            # 1. INFORMACIÓN DEL ESTUDIANTE
            self.log(self.lang_manager.get_string("log_info_header"), "header")
            self.log(self.lang_manager.get_string("log_name", parsed['student_name']) + "\n", "info")

            start_time = None
            for msg in parsed['log_messages']:
                if 'Project folder selected:' in msg:
                    start_time = msg.split(' - ')[0]
                    break
            if start_time:
                self.log(self.lang_manager.get_string("log_start_time", start_time), "info")

            # 2. VALIDACIÓN DE HASH
            self.log(self.lang_manager.get_string("log_hash_header"), "header")

            calculated_hash = self.calculate_resume_hash(self.zip_path, parsed['student_name'], parsed['log_messages'])
            hash_matches = calculated_hash == parsed['declared_hash']
            if hash_matches:
                self.log(self.lang_manager.get_string("log_hash_ok"), "success")
                self.log(self.lang_manager.get_string("log_hash_declared", parsed['declared_hash']) + "\n")
                self.log(self.lang_manager.get_string("log_hash_calculated", calculated_hash) + "\n\n")
            else:
                self.log(self.lang_manager.get_string("log_hash_error"), "error")
                self.log(self.lang_manager.get_string("log_hash_declared", parsed['declared_hash']) + "\n", "error")
                self.log(self.lang_manager.get_string("log_hash_calculated", calculated_hash) + "\n", "error")
                self.log(self.lang_manager.get_string("log_hash_diff",
                                                      abs(calculated_hash - parsed['declared_hash'])) + "\n", "error")
                critical_error = True

            # 3. COMPARACIÓN DE SNAPSHOT INICIAL
            self.log(self.lang_manager.get_string("log_snapshot_header"), "header")

            snapshot = self.extract_initial_snapshot(parsed['log_messages'], project_folder)
            self.log(self.lang_manager.get_string("log_snapshot_files", len(snapshot)) + "\n")

            if self.reference_folder:
                self.log(self.lang_manager.get_string("log_comparing_ref") + "\n", "info")
                differences = self.compare_with_reference(snapshot, self.reference_folder)
                if differences:
                    self.log(self.lang_manager.get_string("log_diff_count_error", len(differences)) + "\n", "warning")
                    for diff in differences:
                        self.log(self.lang_manager.get_string("log_diff_file", diff['file']) + "\n", "warning")
                        self.log(self.lang_manager.get_string("log_diff_size", diff['expected_size'],
                                                              diff['actual_size']) + "\n")
                        self.log(self.lang_manager.get_string("log_diff_lines", diff['expected_lines'],
                                                              diff['actual_lines']) + "\n")
                    critical_error = True
                else:
                    self.log(self.lang_manager.get_string("log_snapshot_ok"), "success")
            else:
                self.log(self.lang_manager.get_string("log_no_ref"), "warning")

            # 4. VALIDACIÓN DE ARCHIVOS DE BACKUP
            self.log(self.lang_manager.get_string("log_backup_header"), "header")

            backup_folder = self.find_backup_folder(self.temp_dir)
            backup_hashes = self.extract_backup_hashes(parsed['log_messages'])

            self.log(self.lang_manager.get_string("log_backup_expected", len(backup_hashes)) + "\n")

            if not backup_hashes:
                if not backup_folder:
                    self.log(self.lang_manager.get_string("log_backup_found_none"), "info")
                else:
                    self.log(self.lang_manager.get_string("log_backup_folder_error"), "warning")
            elif backup_folder:
                validation_results = self.validate_backup_files(backup_folder, backup_hashes)
                failed = [r for r in validation_results if not r.get('matches', False) and 'error' not in r]
                errors = [r for r in validation_results if 'error' in r]

                if failed or errors:
                    self.log(self.lang_manager.get_string("log_backup_count_error", len(failed) + len(errors)) + "\n",
                             "error")
                    for result in errors:
                        self.log(self.lang_manager.get_string("log_backup_file_error", result['file'],
                                                              result['error']) + "\n", "error")
                    for result in failed:
                        self.log(
                            self.lang_manager.get_string("log_backup_hash_error", result['file'], result['expected'],
                                                         result['calculated']) + "\n", "error")
                    critical_error = True
                else:
                    self.log(self.lang_manager.get_string("log_backup_ok"), "success")
            else:
                self.log(self.lang_manager.get_string("log_backup_folder_error"), "error")
                critical_error = True

            # Obtener todos los eventos de actividad
            suspicious_lines, suspicious_events, network_events, unauthorized_app_events = self.analyze_log_activity(
                parsed['log_messages'])

            # 5. ACTIVIDAD SOSPECHOSA (INTERNET ACTIVO)
            self.log(self.lang_manager.get_string("log_suspicious_header"), "header")
            self.log(self.lang_manager.get_string("log_suspicious_lines", suspicious_lines) + "\n")

            if suspicious_lines > 10:
                self.log(self.lang_manager.get_string("log_suspicious_limit_error") + "\n", "error")
                self.log(self.lang_manager.get_string("log_suspicious_events_count", len(suspicious_events)) + "\n",
                         "warning")
                if suspicious_events:
                    self.log(self.lang_manager.get_string("log_suspicious_event"), "warning")
                    for event in suspicious_events:
                        self.log(self.lang_manager.get_string("log_suspicious_event_item", event) + "\n", "warning")
                critical_error = True
            else:
                self.log(self.lang_manager.get_string("log_suspicious_ok"), "success")

            self.log(self.lang_manager.get_string("log_network_header"), "header")

            if network_events:
                self.log(self.lang_manager.get_string("log_network_count", len(network_events)) + "\n", "warning")
                for event in network_events:
                    self.log(self.lang_manager.get_string("log_network_item", event) + "\n", "warning")

            else:
                self.log(self.lang_manager.get_string("log_network_ok"), "success")

            # 6. APLICACIONES NO AUTORIZADAS DETECTADAS (NUEVA SECCIÓN)
            self.log(self.lang_manager.get_string("log_unauthorized_app_header"), "header")

            if unauthorized_app_events:
                self.log(
                    self.lang_manager.get_string("log_unauthorized_app_count", len(unauthorized_app_events)) + "\n",
                    "warning")
                for event in unauthorized_app_events:
                    self.log(self.lang_manager.get_string("log_unauthorized_app_item", event) + "\n", "warning")
                # Las detecciones de apps no autorizadas son un error crítico
                critical_error = True
            else:
                self.log(self.lang_manager.get_string("log_unauthorized_app_ok"), "success")

            # 7. RESUMEN FINAL
            self.log("\n" + self.lang_manager.get_string("log_summary_header"), "header")

            has_backups = False
            if 'backup_hashes' in locals() and backup_hashes:
                has_backups = len(backup_hashes) > 0

            if critical_error:
                self.log(self.lang_manager.get_string("log_summary_error"), "error")
            elif has_backups:
                self.log(self.lang_manager.get_string("log_summary_warning"), "warning")
            else:
                self.log(self.lang_manager.get_string("log_summary_ok"), "success")

        except Exception as e:
            self.log(self.lang_manager.get_string("log_general_error", str(e)), "error")
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
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExamValidator(root)
    root.mainloop()