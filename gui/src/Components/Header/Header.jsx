import Container from "react-bootstrap/Container";

import Navbar from "react-bootstrap/Navbar";

const Header = () => {
  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand
          style={{
            alignContent: "center",
            display: "flex",
            fontFamily: "ui-serif",
            fontSize: "40px",
          }}
          href="#Sa7a7LY"
        >
          Sa7a7LY
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
};

export default Header;
