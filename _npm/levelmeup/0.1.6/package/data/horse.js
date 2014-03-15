const fs = require('fs')
    , csv2 = require('csv2')
    , through2 = require('through2')

var horsejs = []

fs.createReadStream('horse_js.csv')
  .pipe(csv2())
  .pipe(through2({ objectMode: true }, function (chunk, enc, callback) {
    if (chunk.length < 3)
      return callback()

    var datea = chunk[2].split(',')
      , date

    if (datea.length != 3)
      return callback()

    date = new Date(datea[2].trim() + '-' + datea[1].trim() + ' ' + datea[0].trim() + ' GMT+0600')

    this.push({
        id    : chunk[0]
      , tweet : chunk[1]
      , date  : date
    })

    callback()
  }))
  .on('data', function (data) {
    horsejs.push(data)
  })
  .on('end', function () {
    fs.writeFileSync('horse_js.json', JSON.stringify(horsejs), 'utf8')
  })
