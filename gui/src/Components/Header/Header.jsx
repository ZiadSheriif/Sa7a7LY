import Container from "react-bootstrap/Container";

import Navbar from "react-bootstrap/Navbar";

const Header = () => {
  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand
          style={{ alignContent: "center", display: "flex" }}
          href="#Auto-Fiiler"
        >
          Auto Filler
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
};

export default Header;
