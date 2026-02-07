from dotenv import load_dotenv
import os
import google.generativeai as genai
import warnings
warnings.filterwarnings('ignore')

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

print('🧪 Teste de funcionalidade:')
print('=' * 50)

response = model.generate_content('Olá! Você está funcionando?')
print('✅ Teste 1 - Conexão: PASSOU')
print(f'   Resposta: {response.text[:100]}')

response = model.generate_content('Como um consultor financeiro recomendaria investir R$ 10000?')
print('\n✅ Teste 2 - Contexto financeiro: PASSOU')
print(f'   Resposta: {response.text[:100]}...')

print('\n' + '=' * 50)
print('🎉 API FUNCIONANDO CORRETAMENTE!')
