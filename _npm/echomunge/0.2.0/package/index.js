var tokenizer          = /((?:ht|f)tps?\:\/\/[^\s]+|[\w\-]+'[\w\-]+|[^\w\-])/gi
  , sentencizer        = /[\.\!\?]/g
  , ignoreWords        = [ 'RT', '(', ')', '\'', '"', '`' ]
  , sortedSelectWeight = 2 // exponent for Math.rand()
  , spacere            = /^\s+$/
  , maxLength          = 300 // characters
  , useTrippletProbablity = 0.6

  , addFollowerMember  = function (str, space) {
      var key  = '$' + str
      ;(this.followers[key] || (this.followers[key] = new Follower(str))).update(space)
      this.totalFollows++
    }

  , sortedFollowingsMember = function () {
      return Object.keys(this.followers).sort(function (a, b) {
        return this.followers[b].count - this.followers[a].count
      }.bind(this))
    }

  , terminate = function (s) {
      if (/[\.\?\!]$/.test(s)) return s
      var r = Math.random()
      if (r < 0.8) return s + '.'
      if (r < 0.9) return s + '!'
      return s + '?'
    }

  , Follower = (function () {
      function Follower (str) {
        this.str          = str
        this.spaces       = 0
        this.count        = 0
        this.followers    = []
        this.totalFollows = 0
      }
      Follower.prototype = {
          update: function (space) {
            this.count++
            space && this.spaces++
          }

        , spaceProbability: function () {
            return this.spaces / this.count
          }

        , addFollower: addFollowerMember
        , sortedFollowings: sortedFollowingsMember
      }
      return Follower
    }())

  , Word = (function () {
      function Word (str) {
        this.str          = str
        this.terminal     = 0
        this.start        = 0
        this.prespace     = 0
        this.postspace    = 0
        this.followers    = {}
        this.totalFollows = 0
        this.count        = 0
      }

      Word.prototype = {
          addFollowerFollower: function (str, followerStr) {
            var follower = this.followers['$' + str]
            if (!!follower)
              follower.addFollower(followerStr)
          }

        , update: function (terminal, start, prespace, postspace) {
            terminal  && this.terminal++
            start     && this.start++
            prespace  && this.prespace++
            postspace && this.postspace++
            this.count++
          }

        , terminalProbability: function () {
            return this.terminal / this.count
          }

        , prespaceProbability: function () {
            var c = this.count - this.start
            return c ? this.prespace / (this.count - this.start) : 0
          }

        , postspaceProbability: function () {
            var c = this.count - this.terminal
            return c ? this.postspace / (this.count - this.terminal) : 0
          }

        , chooseFollower: function (previous) {
            var sorted, r

            if (this.totalFollows === 0) return null

            sorted = (previous && Math.random() < useTrippletProbablity ? previous.followers['$' + this.str] : this).sortedFollowings()

            r = Math.pow(Math.random(), sortedSelectWeight)
            r = Math.min(sorted.length - 1, Math.round(r * sorted.length))

            return this.followers[sorted[r]]
          }

        , toString: function () { return this.str }

        , addFollower: addFollowerMember
        , sortedFollowings: sortedFollowingsMember
      }

      return Word
    }())

  , Selection = (function () {
      function Selection (db, inp) {
        if (inp instanceof Follower) {
          this.word = db.get(inp.str)
          this.follower = inp
        } else
         this.word = db.get(inp)
      }

      Selection.prototype = {
          toString: function () {
            return this.word.str
          }

        , spaceProbability: function () {
            return this.follower ? this.follower.spaceProbability() : 0
          }

        , terminalProbability: function () {
            return this.word.terminalProbability()
          }
      }

      return Selection
    }())


  , Database = (function () {
      function Database () {
        this.db     = {}
        this.starts = []
        this.sentenceLengths = []
      }

      Database.prototype = {
          get: function (word) {
            return this.db['$' + word]
          }

        , set: function (word) {
            this.db['$' + word.str] = word
            return word
          }

        , recordText: function (text) {
            text
              .split(sentencizer)
              .forEach(function (sentence) {
                sentence = sentence.trim()
                if (sentence.length)
                  this.recordSentence(sentence)
              }.bind(this))
          }

        , recordSentence: function (text) {
            var i = 1
              , data = text.split(tokenizer).filter(function (w) { return w.length })
              , start = false
              , word, lastword, wt

            this.sentenceLengths.push(data.length)

            for (; i <= data.length; i++) {
              wt = data[i - 1].trim()

              if (wt.length === 0)
                continue
              if (ignoreWords.indexOf(wt) > -1) {
                word = lastword = null
                continue
              }

              if (!!word) {
                word.addFollower(wt, i > 1 && spacere.test(data[i - 2]))
                if (!!lastword)
                  lastword.addFollowerFollower(word.str, wt)
              }

              if (!start) {
                start = true
                this.starts.indexOf(wt) == -1 && this.starts.push(wt)
              }

              lastword = word
              word = this.get(wt) || this.set(new Word(wt))
              word.update(
                  i == data.length
                , i > 1
                , i > 1 && spacere.test(data[i - 2])
                , i != data.length && spacere.test(data[i])
              )
            }
          }

        , _maxWords: function (maxLength) {
            return maxLength / 5 // stab in the dark at the maximum number of words needed for the number of characters
          }

        , hasData: function () {
            return this.starts.length > 0
          }

        , makeText: function (options) {
            var words = []
              , w, s
              , _maxLength = options && !!options.maxLength ? options.maxLength : maxLength
              , maxWords = this._maxWords(_maxLength)

            if (!this.hasData()) return ''

            words.push(new Selection(this, (function (starts) {
                var r = Math.min(starts.length - 1, Math.round(Math.random() * starts.length))
                return starts.length ? starts[r] : null
              }(this.starts))))

            while (true) {
              w = words[words.length - 1].word.chooseFollower(
                words.length > 1 ? words[words.length - 2].word : null
              )
              if (!w) break
              words.push(new Selection(this, w))
              if (words.length > maxWords) break
            }

            s = this.stringify(words, _maxLength)
            if (options && options.terminate)
              s = terminate(s)
            return s
          }

        , stringify: function (words, maxLength) {
            var s = ''
              , i

            for (i = 0; i < words.length; i++) {
              if (words[i].spaceProbability() > 0)
                s += ' '
              s += words[i].toString()
              if (words[i].terminalProbability() > 0
                    && (s.length > maxLength * 0.9
                        || Math.random() * (s.length / maxLength) > 1 - words[i].terminalProbability()))
                break
            }

            return s
          }
      }

      return Database
    }())

module.exports = Database