# Image Node.js légère
FROM node:18-alpine

# Dossier de travail
WORKDIR /app

# Installation des dépendances
COPY package*.json ./
RUN npm install

# Copie du code source
COPY . .

# Exposition du port
EXPOSE 3000

# Démarrage du serveur React en mode réseau
CMD ["npm", "start", "--", "--host", "0.0.0.0"]
