import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';

import Manifesto from './Manifesto';
import GettingStarted from './GettingStarted';
import Repos from './Repos';
import About from './About';


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

function loggedIn() {
    return false;
}

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
}));

export default function TabNav({host, domain, repos}) {
  const classes = useStyles();
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  var tabs = [
    <Tab label="Mission" {...a11yProps(0)} />,
    <Tab label="Getting Started" {...a11yProps(1)} />,
    <Tab label="About" {...a11yProps(2)} />
  ]

  var tabPanels = [
      <TabPanel value={value} index={0}>
        <Manifesto host={host} domain={domain}/>
      </TabPanel>,
      <TabPanel value={value} index={1}>
        <GettingStarted host={host} domain={domain}/>
      </TabPanel>,
      <TabPanel value={value} index={2}>
        <About/>
      </TabPanel>,
      <TabPanel value={value} index={3}>
        <Repos repos={repos} />
      </TabPanel>
  ]

  if (loggedIn()) {
    tabs.push(<Tab label="Your Repositories" {...a11yProps(3)} />)
  } else {
    // tabs.push(<Tab label="login" href="/github/login"/>)
  }

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
          {tabs}
        </Tabs>
      </AppBar>
      {tabPanels}
    </div>
  );
}