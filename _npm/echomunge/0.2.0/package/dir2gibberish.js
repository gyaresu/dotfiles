const fs        = require('fs')
    , path      = require('path')
    , EchoMunge = require('./')

var db = {}

function feed (db, options, p) {
  var stat = fs.lstatSync(p)

  if (stat.isFile() && options.fileReg.test(p))
    return db.recordText(fs.readFileSync(p, 'utf8'))

  if (!stat.isDirectory() || stat.isSymbolicLink() || p[0] == '.')
    return

  fs.readdirSync(p).forEach(function (file) {
    feed(db, options, path.join(p, file))
  })
}

function random (dir, options) {
  if (!options)
    options = {}
  if (typeof options.maxLength != 'number')
    options.maxLength = 1000
  if (typeof options.terminate == 'undefined')
    options.terminate = true
  if (!(options.fileReg instanceof RegExp))
    options.fileReg = /(readme)|(\.txt$)/i

  if (!db[dir]) {
    db[dir] = new EchoMunge()
    feed(db[dir], options, dir)
  }

  var txt
  do {
    txt = db[dir].makeText(options)
  } while (!txt)
  return txt
}

module.exports = random