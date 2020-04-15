import React from 'react';


function Manifesto(host, domain, paypalId) {
    return (
        <div>
            <p>
            Graphs (aka diagrams) convey a lot of information quickly. Making them and keeping them up-to-date
            with a coding project is a different story.
            </p>

            <p>
            <code>`pointillism`</code> is not just an <a href="https://github.com/trevorgrayson/pointillism">open source project</a>,
             or a service.  It's a different way to express yourself.
            </p>
            <p>
            GitHub <code>README</code>`s become instantly understandable with diagrams. Wikis stay up to date when they
            point to <code>pointillism's</code> checked-in links.
            When you have your diagrams checked into github, with the project, you can defend your documentation from getting out of date during Pull Reviews.
            </p>

            <h2>Getting Started</h2>

            <p>
              No app installation is necessary, just start using pointillism urls in your documentation.&nbsp;
              <code>`pointillism``</code> image urls reflect github s <code>raw</code> content urls, so you can simply switch the domain to get started.
            </p>

            <p>
              If I have the github link of <code>https://raw.githubusercontent.com/trevorgrayson/pointillism/master/example.dot</code> I
              may just replace <code>`host`</code> with <code>`domain`</code>.
            </p>

            <div class="example">
              <p>
                <code>&lt;img src="https://`domain`/trevorgrayson/pointillism/master/example.dot.svg"/&gt;</code>
              </p>
              <div>
                <img src="https://`domain`/trevorgrayson/pointillism/master/example.dot.svg"/>
              </div>
            </div>

            <h2>As a Service</h2>

            <p>
              If you want to help keep this economy going during these COVID-19 times, please consider paying a small fee for the hosting services.
              <b>Early adopters will be favored.</b>
            </p>
            <p>
              <code>pointillism</code> is and always will be <a href="https://github.com/trevorgrayson/pointillism">open source</a>.
            </p>
            <br/>
            <br/>
            <div id="paypal-button-container"></div>
            <script src="https://www.paypal.com/sdk/js?client-id=`paypalId`&currency=USD" data-sdk-integration-source="button-factory"></script>
        </div>
    )

}

export default Manifesto;