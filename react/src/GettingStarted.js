import React from 'react';
import Typography from '@material-ui/core/Typography';

function rawUrl(host, org, username, path) {
    return "https://{host}/{org}/{username}/raw/{path}"
}

function GettingStarted({host, domain, paypalId}) {
    return (
        <Typography align="left" paragraph={true}>
            <h1>Github.com</h1>
            <p>
            All dot files hosted in <a href="https://github.com">github.com</a> repositories are supported.
            </p>

            <h2>open repositories</h2>
            <p>
            If your repository is open to the world, then <code>pointillism.io</code> is free.
            </p>

            <h2>private repositories</h2>
            <p>
            If your repository is private, please consider subscribing. The cost is reasonable, and
            based on the honor system presently.
            </p>

            <h2>getting your pointillism url</h2>
            <p>
            No installation is necessary to get <code>pointillism.io</code> hosted dot graphs!
            By changing the domain on your "raw" github dot file URLs you'll be rendering in no time.
            </p>
            <p>
                <code>
                   https://raw.githubusercontent.com/trevorgrayson/pointillism/master/pointillism.dot
                </code>
            </p>
            <p>becomes...</p>
            <p>
                <code>
                    https://pointillism.io/trevorgrayson/pointillism/master/pointillism.dot.svg
                </code>
            </p>
            <center>
                <img src="https://pointillism.io/trevorgrayson/pointillism/master/pointillism.dot.svg"/>
            </center>

            <h3>step by step</h3>
            <ol className="steps">
                <li>Ensure you're logged into your <a href="https://github.com/login">github account</a>.</li>
                <li>
                    Navigate to the repository, and to the <code>.dot</code> graph file you would like to render.<br/>
                    For example: <a href="https://github.com/trevorgrayson/pointillism/blob/master/pointillism.dot">example.dot</a></li>
                <li>Click on the "Raw" button located to the top right, close to the edit buttons.</li>
                <li>You'll be forwarded to a new URL, which you will modify to render your image.</li>
                <li>
                    <b>!!!</b>&nbsp;
                    If you repository is private, this link will have a token. Be sure to include this token.&nbsp;
                    <b>!!!</b>
                </li>
                <li>Change the domain on this URL to <code>pointillism.io</code>.</li>
                <li>
                    Append an image file type to the full url.  Supported formats include:
                    <code>.svg</code>, <code>.png</code>, <code>.jpg</code>

                </li>
            </ol>
            <h2>including images in <code>README.md</code></h2>
            <p>Find your <code>pointillism.io</code> link (as described in the previous section) and add a markdown
            image tag as described in <a href="https://guides.github.com/features/mastering-markdown/">Github's Mastering Markdown</a>.
            </p>
            <p>
                <code>![pointillism.io](https://pointillism.io/trevorgrayson/pointillism/master/pointillism.dot.svg)</code>
            </p>

        </Typography>
    )
}

export default GettingStarted;