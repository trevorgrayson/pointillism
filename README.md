# pointillism

[DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) file rendering/embedding as a Service.
Be expressive in your documentation with diagrams.

![https://travis-ci.com/trevorgrayson/pointillism/](https://travis-ci.com/trevorgrayson/pointillism.svg?branch=master)


### Embedding [DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) Graphs in Github

```
![pointillism.dot](https://pointillism.io/trevorgrayson/pointillism/master/pointillism.dot.svg)
```

![pointillism.dot](https://pointillism.io/trevorgrayson/pointillism/master/pointillism.dot.svg)


### [PlantUML](https://plantuml.com/) is in Beta Testing!

![beta PlantUML](https://pointillism.io/trevorgrayson/pointillism/blob/master/resources/plant/pointillism.pu.svg)

## Making a request

`pointillism.io` links mirror github urls.  Replace the domain in your github hosted diagrams 
to render in github, wikis, etc!


e.g. `http://pointillism.io/{username}/{project}/{filepath}.{format}` will render that dotfile as a PNG.

github's `token` parameter will also pass through if you put it in the query string

```
http://pointillism.io/{username}/{project}/{filepath}.{format}?token=XYZ
```

## Makefile

This project's lifecycle (`compile`, `test`, `server`) is managed in its [Makefile](https://github.com/trevorgrayson/pointillism/blob/master/Makefile).

pointillism is open source.
