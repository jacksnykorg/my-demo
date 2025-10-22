# Using a full-sized Node image to trigger Snyk IaC recommendations
FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD [ "node", "index.js" ]