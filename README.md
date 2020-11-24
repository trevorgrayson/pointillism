# pointillism ![build status](https://circleci.com/gh/pointillism/pointillism.svg?style=svg)

[DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) file rendering/embedding as a Service.
Be expressive in your documentation with diagrams.

### Embedding [DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) Graphs in Github

```
![pointillism.dot](https://pointillism.io/pointillism/pointillism/master/pointillism.dot.svg)
```

![pointillism.dot](https://pointillism.io/pointillism/pointillism/master/pointillism.dot.svg)


### [PlantUML](https://plantuml.com/) is in Beta Testing!

![beta PlantUML](https://pointillism.io/pointillism/pointillism/blob/master/resources/plant/pointillism.pu.svg)

## Making a request

`pointillism.io` links mirror github urls.  Replace the domain in your github hosted diagrams 
to render in github, wikis, etc!


e.g. `http://pointillism.io/{username}/{project}/{filepath}.{format}` will render that dotfile as a PNG.

github's `token` parameter will also pass through if you put it in the query string

```
http://pointillism.io/{username}/{project}/{filepath}.{format}?token=XYZ
```

## Makefile

This project's lifecycle (`compile`, `test`, `server`) is managed in its [Makefile](https://github.com/pointillism/pointillism/blob/master/Makefile).

pointillism is open source.

## Docker

Run this project yourself:

```
    docker run -e GITHUB_TOKEN=xxx pointillism/pointillism
```

You may optionally add a `HOST` env variable and change the github server that pointillism pulls files from.


[
![pointillism.io](https://pointillism.io/trevorgrayson/pointillism/master//tmp/pointillism_prs/trevorgrayson/pointillism/other-branch.dot.svg?theme=auto)
](https://pointillism.io/trevorgrayson/pointillism/master//tmp/pointillism_prs/trevorgrayson/pointillism/other-branch.dot.html)

[
![pointillism.io](https://pointillism.io/trevorgrayson/pointillism/master//tmp/pointillism_prs/trevorgrayson/pointillism/example.dot.svg?theme=auto)
](https://pointillism.io/trevorgrayson/pointillism/master//tmp/pointillism_prs/trevorgrayson/pointillism/example.dot.html)

[
![pointillism.io](https://pointillism.io/trevorgrayson/pointillism/master//tmp/pointillism_prs/trevorgrayson/pointillism/pointillism.dot.svg?theme=auto)
](https://pointillism.io/trevorgrayson/pointillism/master//tmp/pointillism_prs/trevorgrayson/pointillism/pointillism.dot.html)

Learn more about ![pointillism.io](https://pointillism.io).
