import React from 'react';
import Typography from '@material-ui/core/Typography';

function Manifesto({host, domain, paypalId}) {
    const imageUrl = `https://${domain}/trevorgrayson/pointillism/master/example.dot.svg`
    return (
        <Typography align="left" paragraph={true}>
            <p>
            Graphs (aka diagrams) convey a lot of information quickly. Making them and keeping them up-to-date
            with a coding project is a different story.
            </p>

            <p>
            <code>`pointillism.io`</code> is not just an <a href="https://github.com/trevorgrayson/pointillism">open source project</a>,
             or a service.  It's a different way to express yourself.
            </p>

            <ul>
              <li>GitHub <code>README</code>s become instantly understandable with diagrams.</li>
              <li>Wikis stay up to date when they point to <code>pointillism's</code> checked-in links.</li>
            </ul>

            <p>
            When you have your diagrams checked into github <b>with the project</b>, you can defend your documentation
            from getting out of date during Pull Reviews.
            </p>

            <h2>Getting Started</h2>
            <p>
              No app installation is necessary. Check in <a href="https://en.wikipedia.org/wiki/DOT_(graph_description_language)">dot graph files</a> and start using pointillism urls in your documentation.&nbsp;
              <code>pointillism.io</code> image urls reflect github's <code>raw</code> content urls, so it's easy getting started.
            </p>
            <p>
              If you have a github file such as <code>https://{host}/trevorgrayson/pointillism/master/example.dot</code>,
              just replace <code>{host}</code> with <code>{domain}</code>, and append your desired format (<code>.svg</code>, <code>.png</code>, <code>.jpg</code>).
            </p>

            <div class="example">
              <p>
                <code>&lt;img src="{imageUrl}"/&gt;</code>
              </p>
              <center>
                <img src={imageUrl}/>
              </center>
            </div>
        </Typography>
    )

}

export default Manifesto;