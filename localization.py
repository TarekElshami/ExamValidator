import os
import json

class LocalizationManager:
    """Clase para gestionar el idioma."""
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
                "log_unauthorized_app_header": "\n" + "=" * 80 + "\n6. APLICACIONES NO AUTORIZADAS DETECTADAS\n" + "=" * 80 + "\n",
                "log_unauthorized_app_count": "⚠ {} aplicación(es) no autorizada(s) detectada(s):",
                "log_unauthorized_app_item": "  - {}",
                "log_unauthorized_app_ok": "✓ No se detectaron aplicaciones no autorizadas\n",
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
                "log_unauthorized_app_header": "\n" + "=" * 80 + "\n6. UNAUTHORIZED APPLICATIONS DETECTED\n" + "=" * 80 + "\n",
                "log_unauthorized_app_count": "⚠ {} unauthorized application(s) detected:",
                "log_unauthorized_app_item": "  - {}",
                "log_unauthorized_app_ok": "✓ No unauthorized applications detected\n",
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