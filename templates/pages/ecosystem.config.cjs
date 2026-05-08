module.exports = {
  apps : [{
    name: "{{ domain }}",
    script: "./app.js",
    env: {
      NODE_ENV: "production",
    }
  }]
}
