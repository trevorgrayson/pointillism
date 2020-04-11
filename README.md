# pointillism
[DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) file rendering/embedding as a Service.

![https://travis-ci.com/trevorgrayson/pointillism/](https://travis-ci.com/trevorgrayson/pointillism.svg?branch=master)

## Making a request

You MUST append a 3 character `.{format}`.  (e.g. svg, png, jpg)

e.g. `http://pointillism.io/{username}/{project}/{filepath}.{format}` will render that dotfile as a PNG.

github's `token` parameter will also pass through if you put it in the query string

```
http://pointillism.io/{username}/{project}/{filepath}.{format}?token=XYZ
```

## serverless

A serverless configuration is included, and presently points to `https://raw.githubusercontent.com`. Configured this way,
you can render any dotfile that's being hosted publically on github.com. 

e.g. `http://your-host.com/{username}/{project}/{filepath}` will render that dotfile as a PNG.

## Running Locally

```
HOST=https://raw.githubusercontent.com make server
```

### Docker

```
  docker run tgrayson/pointillism
```

## cli

```
python -m point example.dot
```

## Hosted

`http://pointillism.io/trevorgrayson/pointillism/master/example.dot.svg`

![example.dot](http://pointillism.io/trevorgrayson/pointillism/master/example.dot.svg)
Embedding [DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) files as a Service.
