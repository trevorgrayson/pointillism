import React from 'react';
import Typography from '@material-ui/core/Typography';

// function rawUrl(host, org, username, path) {
//     return "https://{host}/{org}/{username}/raw/{path}"
// }

function GettingStarted({host, domain, paypalId}) {
    const ptImage = 'https://pointillism.io/trevorgrayson/pointillism/master/pointillism.dot.svg';

    return (
        <Typography align="left" paragraph={true}>
            <h1>Github.com</h1>
            <p>
            All dot files hosted in <a href="https://github.com">github.com</a> repositories are supported.
            </p>

            <h2>rendering images in <code>README.md</code> and Wikis.</h2>
            <p>Find your <code>pointillism.io</code> link (as described in the previous section) and add a markdown
            image tag as described in <a href="https://guides.github.com/features/mastering-markdown/">Github's Mastering Markdown</a>.
            </p>
            <p>
                <code>![pointillism.io](https://pointillism.io/trevorgrayson/pointillism/master/pointillism.dot.svg)</code>
            </p>

            <h2>rendering using &lt;img\/&gt; tags</h2>

            <p>
                <code>&lt;img src="https://pointillism.io/trevorgrayson/pointillism/master/pointillism.dot.svg" /&gt;</code>
            </p>

            <h2>getting your pointillism url</h2>
            <p>
            Hosting your diagrams on <code>pointillism.io</code> is as easy as linking to your github account!
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
                <img src="https://pointillism.io/trevorgrayson/pointillism/master/pointillism.dot.svg" alt="pointillism architecture" />
            </center>
            <h3>step by step</h3>
            <ol className="steps">
                <li>Ensure you're logged into your <a href="https://github.com/login">github account</a>.</li>
                <li>
                    Navigate to the repository, and to the <code>.dot</code> graph file you would like to render.<br/>
                    For example: <a href="https://github.com/trevorgrayson/pointillism/blob/master/pointillism.dot">example.dot</a></li>
                <li>Click on the "Raw" button located to the top right, close to the edit buttons.</li>
                <li>You'll be forwarded to a new URL, which you will modify to render your image.</li>
                <li>Change the domain on this URL to <code>pointillism.io</code>.</li>
                <li>
                    Append an image file type to the full url.  Supported formats include:
                    <code>.svg</code>, <code>.png</code>, <code>.jpg</code>
                </li>
            </ol>
            <h3>authorization</h3>
            <p>To render files from a private repo, you must give pointillism.io access to the file.  This
            can be done using github's temporary <code>raw</code> tokens, or by creating a Repository Token to be shared.
            </p>
            <h3>Raw Token</h3>
            <p>This method may be less preferred because <strong>github's user content tokens are temporary</strong>
            (they seem to last 7 days.)
            </p>

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
        </Typography>
    )
}

export default GettingStarted;