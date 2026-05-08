const http = require('http');

const port = {{ port }};
const domain = '{{ domain }}';

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end(`API is running for ${domain} on port ${port}\n`);
});

server.listen(port, () => {
  console.log(`Server running at http://127.0.0.1:${port}/`);
});
