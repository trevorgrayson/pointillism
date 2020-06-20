import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';

import Manifesto from './Manifesto';
import Account from './Account';
import GettingStarted from './GettingStarted';
import Repos from './Repos';
import About from './About';
import PayPalConfirm from './payments/PayPalConfirm'

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";


function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </Typography>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function loggedIn(username) {
    return username !== undefined && username.length > 0;
}

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
}));

export default function TabNav({host, domain, repos, username}) {
  const classes = useStyles();
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  var tabs = []
  let routes = [];

  if (loggedIn(username)) {
    tabs.push(<Tab label="Your Repositories" component={Link} to="/repos" />)
    tabs.push(<Tab label="Account" href="/account" />)

    routes = [
      <Route path="/account"><Account name={username} /></Route>,
      <Route path="/repos"><Repos repos={repos} /></Route>,
    ];
  } else {
    tabs.push(<Tab label="login" href="/github/login"/>)
  }

  routes = [...routes, ...[
    <Route path="/paypal/confirm" component={PayPalConfirm} />,
    <Route path="/getting-started"><GettingStarted host={host} domain={domain}/></Route>,
    <Route path="/about"><About/></Route>,
    <Route path="/"><Manifesto host={host} domain={domain}/></Route>,
  ]];

  return (
    <div className={classes.root}>
      <Router>
        <AppBar position="static">
          <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
            <Tab label="Mission" component={Link} to="/" />
            <Tab label="Getting Started" component={Link} to="/getting-started" />
            <Tab label="About" component={Link} to="/about" />
            {tabs}
          </Tabs>
        </AppBar>
        <Switch>{routes}</Switch>
      </Router>
      
    </div>
  );
}
