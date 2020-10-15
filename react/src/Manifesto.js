import React from 'react';
import Typography from '@material-ui/core/Typography';
// import PayPalExpressButton from './payments/PayPalExpressButton'
import Calculator from './Calculator';

function Manifesto({host, domain, paypalId}) {
    const sourceUrl = `https://github.com/trevorgrayson/pointillism/blob/master/pointillism.dot`
    const imageUrl = `https://${domain}/trevorgrayson/pointillism/master/pointillism.dot.svg`
    const dotContent = `digraph Pointillism {
  subgraph cluster_Github {
    label = Github

    DotFile
    README -> Camu
  }
  
  Camu -> Pointillism
    
  Pointillism -> DotFile
    
  Users -> README
}`;

    return (
        <Typography align="left" paragraph={true}>
            <p>
            Graphs (aka diagrams) convey a lot of information quickly. Making them and keeping them up-to-date
            with a coding project is a different story.
            </p>

            <p>
            <code>pointillism.io</code> is not just an <a href="https://github.com/trevorgrayson/pointillism">open source project</a>,
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

            <h2>How it Works</h2>
            <p>
              Check in <a href="https://en.wikipedia.org/wiki/DOT_(graph_description_language)">dot graph files</a>&nbsp;
              to github, like this one describing <code>pointillism</code>'s workflow:
            </p>
            <p class="pointillism-example">
              <code class="dot">{dotContent}</code>
              <h5>Source: <a href={sourceUrl}>{sourceUrl}</a></h5>
            </p>
            <p>
              <code>pointillism.io</code> image urls reflect github's content urls, so just replace the domain for a rendered image.
            </p>
            <div className="example">
              <p class="center">
                <code>&lt;img src="{imageUrl}"/&gt;</code>
                <br/>
                <img src={imageUrl} alt="example graph" />
              </p>
              
              <Calculator />
            </div>
            <p>  
              Start using pointillism urls in your documentation,&nbsp;
              <a href="https://github.com/trevorgrayson/pointillism">just like we do</a>.&nbsp;
            </p>

            <h2>As a Service</h2>
            <p>
              If you want to help keep this economy going during these COVID-19 times,
              please consider paying a small fee for the hosting services. <b>Early adopters will be favored.</b>
            </p>
            <p>
              <code>pointillism</code> is and always will be <a href="https://github.com/trevorgrayson/pointillism">open source</a>.
            </p>
            
        </Typography>
    )
    // <PayPalExpressButton/> 
}

export default Manifesto;
