import threading
import json
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class NexusBetRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(NexusBetRoot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15

        # Título
        self.add_widget(Label(
            text='Nexus-Bet (Quantum + Football)', 
            font_size=20, 
            size_hint_y=None, 
            height=40
        ))

        # Configuração da API Key da IBM Quantum
        self.add_widget(Label(text='Token IBM Quantum:', size_hint_y=None, height=25))
        self.ibm_token_input = TextInput(
            text='mPIg_rIpBe1HwmLKw1onL7-RZwYtCswqCxYBKhbqUbzB',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.ibm_token_input)

        # Configuração da API Key de Futebol
        self.add_widget(Label(text='API Key de Futebol (Opcional/Paga):', size_hint_y=None, height=25))
        self.football_token_input = TextInput(
            text='',
            hint_text='Cole sua chave da API de futebol aqui',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.football_token_input)

        # Status / Log na tela
        self.status_label = Label(
            text='Status: Pronto para configurar e conectar', 
            font_size=13
        )
        self.add_widget(self.status_label)

        # Botão para disparar a computação quântica
        self.btn_calc = Button(
            text='Executar Otimização Quântica', 
            size_hint_y=None, 
            height=55
        )
        self.btn_calc.bind(on_press=self.trigger_quantum_task)
        self.add_widget(self.btn_calc)

    def trigger_quantum_task(self, instance):
        self.btn_calc.disabled = True
        self.status_label.text = 'Status: Enviando job para a IBM Quantum...'

        current_token = self.ibm_token_input.text.strip()
        threading.Thread(target=self.run_quantum_request, args=(current_token,), daemon=True).start()

    def run_quantum_request(self, token):
        try:
            url = "https://api.quantum-computing.ibm.com/api/Network/ibm-q/Groups/open/Projects/main/jobs"

            headers = {
                "X-Access-Token": token,
                "Content-Type": "application/json"
            }

            qasm_code = """
            OPENQASM 2.0;
            include "qelib1.inc";
            qreg q[2];
            creg c[2];
            h q[0];
            cx q[0],q[1];
            measure q[0] -> c[0];
            measure q[1] -> c[1];
            """

            payload = {
                "qObject": None,
                "backend": {"name": "ibmq_qasm_simulator"},
                "shots": 1024,
                "qasm": qasm_code
            }

            response = requests.post(url, headers=headers, json=payload, timeout=15)

            if response.status_code == 200:
                data = response.json()
                job_id = data.get('id', 'Sucesso')
                self.update_ui_safe(f"Sucesso! Job ID: {job_id}")
            else:
                self.update_ui_safe(f"Erro HTTP {response.status_code}: {response.text[:60]}")

        except Exception as e:
            self.update_ui_safe(f"Erro de Conexão: {str(e)}")

    def update_ui_safe(self, message):
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.apply_ui_update(message))

    def apply_ui_update(self, message):
        self.status_label.text = f"Status: {message}"
        self.btn_calc.disabled = False


class NexusBetApp(App):
    def build(self):
        return NexusBetRoot()

if __name__ == '__main__':
    NexusBetApp().run()
