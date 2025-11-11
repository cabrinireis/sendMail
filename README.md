# Sistema de Envio de E-mails em Massa

Este é um script Python simples para enviar e-mails em massa para múltiplos destinatários.

## Pré-requisitos

- Python 3.6 ou superior
- Conta de e-mail com suporte a SMTP (como Gmail, Outlook, etc.)
- Para contas do Gmail, é necessário usar uma "Senha de App" ao invés da senha normal da conta

## Configuração

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Crie um arquivo `.env` baseado no `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Edite o arquivo `.env` com suas credenciais de e-mail:
   - `EMAIL_REMETENTE`: Seu endereço de e-mail
   - `SENHA_APP`: Sua senha de aplicativo (para Gmail) ou senha da conta
   - `SMTP_SERVIDOR` e `SMTP_PORTA`: Configurações do servidor SMTP (opcional, padrão para Gmail)

4. Prepare sua lista de destinatários no arquivo `destinatarios.csv` no formato:
   ```
   email,nome
   email1@exemplo.com,Nome 1
   email2@exemplo.com,Nome 2
   ```

## Como usar

1. Execute o script:
   ```bash
   python envio_emails.py
   ```

2. Siga as instruções na tela para:
   - Inserir o assunto do e-mail
   - Digitar o conteúdo do e-mail (pressione Enter e depois Ctrl+D para finalizar)
   - Confirmar o envio

## Dicas para Gmail

Se estiver usando o Gmail, você precisará:

1. Ativar a verificação em duas etapas na sua conta Google
2. Criar uma "Senha de App" em [Segurança da Conta Google](https://myaccount.google.com/security)
3. Usar esta senha no campo `SENHA_APP`: 'pwcb aumm ckbg nwdl' do arquivo `.env`

## Personalização

Você pode personalizar o conteúdo do e-mail usando variáveis como `{nome}` no corpo do e-mail. Por exemplo:

```
Olá {nome},

Este é um e-mail personalizado para você.

Atenciosamente,
Equipe de Suporte
```

## Notas de Segurança

- Nunca compartilhe seu arquivo `.env` ou credenciais de e-mail
- Para maior segurança, use variáveis de ambiente do sistema ao invés do arquivo `.env` em produção
- Este script é para uso pessoal e não deve ser usado para envio de spam
