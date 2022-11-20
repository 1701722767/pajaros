import { Outlet } from "react-router-dom";
import { Nav, Grid, Row, Col } from "rsuite";
import React from "react";
import { URLContext } from "./contexts/url";
import { Link } from "react-router-dom";

const NavLink = React.forwardRef(({ href, children, ...rest }, ref) => (
  <Link ref={ref} to={href} {...rest}>
    {children}
  </Link>
));

const Layout = () => {

  const [url, setUrl] = React.useState("https://webhook.site/e7a18c97-5316-4b18-8305-62e5ebc6dd9d");
  const value = React.useMemo(
    () => ({ url, setUrl }),
    [url]
  );

  return (
    <Grid fluid>
      <Row>
        <Col xs={24} sm={24} md={12} mdOffset={5}>
          <Nav appearance="subtle" justified>
            <Nav.Item as={NavLink} href="/">
              <h4 className="text-center">Predecir</h4>
            </Nav.Item>
            <Nav.Item as={NavLink} href="/settings">
              <h4 className="text-center">Ajustes</h4>
            </Nav.Item>
          </Nav>
        </Col>
        <Col xs={22} xsOffset={1} sm={22} smOffset={1} md={10} mdOffset={6}>
          <URLContext.Provider value={value}>
            <Outlet />
          </URLContext.Provider>
        </Col>
      </Row>
    </Grid>
  );
};

export default Layout;
