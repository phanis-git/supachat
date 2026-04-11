# FROM node:22
# WORKDIR /app
# COPY . .
# RUN npm install && npm run build
# RUN npm install -g serve
# CMD ["serve", "-s", "build", "-l", "3000"]



# FROM node:22
# WORKDIR /app
# COPY . .
# RUN npm install
# EXPOSE 5173
# CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]


FROM node:22 AS builder
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]