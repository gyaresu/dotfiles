# EchoMunge

Collect text and echo back out text with similar patterns. Pure silliness with no practical purpose. A little like Chinese Whispers but not really.

For Node.js, you'll find EchoMunge in npm as *echomunge*.

See also [EchoMunge-Web](https://github.com/rvagg/node-echomunge-web) for an extension that will munge Wikipedia and other web pages for you.

### Example

```js
var EchoMunge = require('echomunge')
  , db = new EchoMunge()
  , fs = require('fs')
  , body = fs.readFileSync('star_wars_a_new_hope.txt', 'utf8')

db.recordText(body)
for (var i = 0; i < 100; i++)
  console.log(db.makeText({ maxLength: 500, terminate: true }))
```

And you might get something like this:

 > Fighter's above you, motherly woman, fills a pitcher with blue fluid from his shoulder at Luke as the pirateship makes the jump into hyperspace isn't worth the effort.
 > 
 > Well, I can't see his identification?
 > 
 > Threepio intercedes on behalf of laserbolts at the vast Imperial fighters?
 > 
 > Then everything is quiet for a few feet of Luke's voice over the surface and into space dust?
 > 
 > Enemy fighters flying in formation down the main reactor system will dare oppose the best star-pilot in white, the Force if enemy ships are near Han.
 > 
 > What I make the computer screen.
 > 
 > IMPERIAL STARDESTROYER?
 > 
 > Not likely.
 > 
 > Out of its mechanical arms bearing a transport that the TIE ships dive on from the right moment.
 > 
 > Men, monsters, who zaps him with that one thing straight up in range in five minutes to lock it down.
 > 
 > Even I see that.
 > 
 > Aghast, hard, bear-like creatures are done?
 > 
 > WINGMAN'S COCKPIT: DODONNA: The Jedi his power!

**OR** you could use the bundled executable that you'll get if you `npm install echomunge -g` to do the same thing:

```sh
$ echomunge star_wars_a_new_hope.txt 100
```

## API

### EchoMunge

```js
var db = new EchoMunge()
```

Create a new "database" instance to store words, calculate connection probabilities and generate text from the data.

```js
db.recordText(text)
```

Process a slab of text. Store the words and calculation connection probabilities. You can call this as many times as you like with different slabs of text, of any length, at any time, and the results will be aggregated.

```js
db.makeText([options])
```

Generate some text that sounds vaguely like the text that has been processed thus far. Available options are: `maxLength` - the maximum number of characters for the output (number, default `300`), and `terminate` - ensure all generated text is terminated properly (boolean, default `false`).

There's potential for a lot more options to tweak the behaviour, if you want to have a go at exposing them then good luck with that!

## Licence

EchoMunge is Copyright (c) 2012 Rod Vagg [@rvagg](https://twitter.com/rvagg) and licenced under the MIT licence. All rights not explicitly granted in the MIT license are reserved. See the included LICENSE file for more details.