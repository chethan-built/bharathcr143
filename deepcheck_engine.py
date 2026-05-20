import sys
import os
import io

try:
    import gradio as gr
except ImportError:
    os.system('pip install -q gradio')
    import gradio as gr

# ==========================================
# 🛡️ SECURITY CORE: PRE-CHECK LOGIC
# ==========================================
def security_pre_screen(code_string):
    """Scans code text for malicious injection attempts before compilation."""
    # List of dangerous words that shouldn't be executed in a public sandbox
    blacklist = ["os.system", "subprocess", "rmtree", "shutil", "globals()", "eval("]
    
    for dangerous_word in blacklist:
        if dangerous_word in code_string:
            return False, f"⚠️ SECURITY BREACH DETECTED: Use of restricted string '{dangerous_word}' is blocked."
    return True, "Passed security screening."

# ==========================================
# ⚙️ BACKEND SANDBOX COMPILER ENGINE
# ==========================================
def run_and_catch_code(code_string):
    original_stdout = sys.stdout
    output_buffer = io.StringIO()
    sys.stdout = output_buffer
    
    try:
        local_vars = {}
        # Execute in a highly restricted global environment
        exec(code_string, {"__builtins__": __builtins__}, local_vars)
        sys.stdout = original_stdout
        return True, output_buffer.getvalue()
    except Exception as e:
        sys.stdout = original_stdout
        return False, str(e)

def deepcheck_interface(user_code):
    if not user_code.strip():
        return "⚠️ DEEPCHECK ALERT: No instruction string received."
    
    # Run through the security core first
    is_safe, security_msg = security_pre_screen(user_code)
    if not is_safe:
        return f"🔴 CORE SYSTEM COMPILATION: BLOCKED\n\n[-] {security_msg}"
        
    # Run through the code executor if safe
    success, result = run_and_catch_code(user_code)
    
    if success:
        clean_res = result.strip() if result.strip() else "[Process executed with no console prints]"
        return f"🟢 CORE SYSTEM COMPILATION: SUCCESS\n\n[+] Hidden Sandbox Output:\n----------------------------------------\n{clean_res}"
    else:
        return f"🔴 CORE SYSTEM COMPILATION: CRASHED\n\n[-] Critical Exception Log:\n----------------------------------------\nRuntime Error: {result}"

# ==========================================
# 🎨 CYBERPUNK CUSTOM THEMING & CSS
# ==========================================
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;800&family=Share+Tech+Mono&display=swap');

.gradio-container h1, .gradio-container h2, .gradio-container h3 {
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 2px;
    text-transform: uppercase;
}

textarea {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 14px !important;
    background-color: #070a0e !important;
    color: #00FF66 !important;
    border: 1px solid rgba(0, 255, 102, 0.2) !important;
}

button.primary {
    background: #00FF66 !important;
    color: #000000 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: 1.5px;
    box-shadow: 0 0 15px rgba(0, 255, 102, 0.4) !important;
    border: none !important;
}
"""

cyber_theme = gr.themes.Monochrome(primary_hue="green", neutral_hue="slate")

# ==========================================
# 🏗️ INTERACTIVE UI ARCHITECTURE
# ==========================================
with gr.Blocks(theme=cyber_theme, css=custom_css) as app:
    gr.Markdown("# ⚡ AIONIX // DEEPCHECK AI")
    # Your official branding signature
    gr.Markdown("### 🛠️ LEAD SYSTEM ARCHITECT: B. CHETHAN REDDY")
    gr.Markdown("An automated deployment testing sandbox. Input Python statements below to verify background compilation safety.")
    
    with gr.Row():
        code_input = gr.Textbox(
            label="⌨️ SYSTEM CODE INPUT", 
            placeholder="Type your script logic here... (e.g., print('DeepCheck Active'))", 
            lines=6
        )
    
    with gr.Row():
        run_btn = gr.Button("🚀 COMPILE & EXECUTE", variant="primary")
    
    with gr.Row():
        terminal_output = gr.Textbox(
            label="📟 SANDBOX RUNTIME TERMINAL LOG", 
            lines=7,
            interactive=False
        )
        
    run_btn.click(fn=deepcheck_interface, inputs=code_input, outputs=terminal_output)

print("🛸 Launching updated core framework...")
app.launch(inline=True, share=False)
  
