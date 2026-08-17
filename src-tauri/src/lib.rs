#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let mut builder = tauri::Builder::default();


    builder
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
