# pointillism
[DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) file rendering/embedding as a Service.

![https://travis-ci.com/trevorgrayson/pointillism/](https://travis-ci.com/trevorgrayson/pointillism.svg?branch=master)

## serverless

A serverless configuration is included, and presently points to `https://raw.githubusercontent.com`. Configured this way,
you can render any dotfile that's being hosted publically on github.com. 

e.g. `http://your-host.com/{username}/{project}/{filepath}` will render that dotfile as a PNG.

## Running Locally

```
HOST=https://raw.githubusercontent.com make server
```

### Docker

You MUST postpend a 3 character `.{format}`.  (e.g. svg, png, jpg)

e.g. `http://your-host.com/{username}/{project}/{filepath}.{format}` will render that dotfile as a PNG.

```
  docker run tgrayson/pointillism
```


## Hosted

`http://pointillism.necessaryeval.com/trevorgrayson/pointillism/master/example.dot`

![example.dot](http://pointillism.necessaryeval.com/trevorgrayson/pointillism/master/example.dot)
Embedding [DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) files as a Service.
