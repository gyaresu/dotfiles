var concat = require('concat-stream');
var http = require('http');

var server = http.createServer(function (req, res) {
    if (req.method === 'POST') {
        req.pipe(concat(function (body) {
            var obj = JSON.parse(body);
            res.end(Object.keys(obj).join('\n') + '\n');
        }));
    }
    else res.end();
});
server.listen(5000);
