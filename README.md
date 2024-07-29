# Bulk Email Sender

Culk Email Sender is a Python application designed to facilitate sending emails using SendGrid. This README provides information on setting up and configuring the application.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

# Configration

The application uses a .env file to store sensitive configuration details. Create a file named .env in the root directory of the project and include the following environment variables:

2. Set ENV FILE:
   ```bash
   PYTHONHTTPSVERIFY=0
   SECRET_KEY='your-secret-key-here'
   SENDGRID_API_KEY='your-sendgrid-api-key-here'
   SENDGRID_FROM_EMAIL='your-sendgrid-from-email-here'
   ```
