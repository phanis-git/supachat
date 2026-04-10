# FROM node:22
# WORKDIR /app
# COPY . .
# RUN npm install && npm run build
# RUN npm install -g serve
# CMD ["serve", "-s", "build", "-l", "3000"]

FROM node:22

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]