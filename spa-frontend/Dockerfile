# Use a lightweight Node.js image
FROM node:20

WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire project
COPY . .

# Expose the frontend port
EXPOSE 5173

# Run development server
CMD ["npm", "run", "dev"]
