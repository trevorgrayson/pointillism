# pointillism
Embedding [DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) files as a Service.


## serverless

A serverless configuration is included, and presently points to `https://raw.githubusercontent.com`. Configured this way,
you can render any dotfile that's being hosted publically on github.com. 

e.g. `http://your-host.com/{username}/{project}/{filepath}` will render that dotfile as a PNG.

## Running Locally

```
HOST=https://raw.githubusercontent.com make server
```

