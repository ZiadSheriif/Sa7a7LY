import React from "react";
import {
  MDBFooter,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBIcon,
} from "mdb-react-ui-kit";
import {
  AiOutlineTwitter,
  AiFillInstagram,
  AiFillGithub,
  AiFillLinkedin,
} from "react-icons/ai";
import { BsFacebook } from "react-icons/bs";

function Footer() {
  return (
    <MDBFooter bgColor="light" className="text-center text-lg-start text-muted">
      <section className="d-flex justify-content-center justify-content-lg-between p-4 border-bottom">
        <div className="me-5 d-none d-lg-block">
          <span>Get connected with us on social networks:</span>
        </div>

        <div>
          <a href="#1" className="me-4 text-reset">
            <AiOutlineTwitter size={23} />
          </a>
          <a href="#2" className="me-4 text-reset">
            <BsFacebook size={23} />
          </a>
          <a href="#3" className="me-4 text-reset">
            <AiFillInstagram size={23} />
          </a>
          <a href="#4" className="me-4 text-reset">
            <AiFillGithub size={23} />
          </a>
          <a href="#5" className="me-4 text-reset">
            <AiFillLinkedin size={23} />
          </a>
        </div>
      </section>

      <section className="">
        <MDBContainer className="text-center text-md-start mt-5">
          <MDBRow className="mt-3">
            <MDBCol md="3" lg="4" xl="3" className="mx-auto mb-4">
              <h6 className="text-uppercase fw-bold mb-4">
                <MDBIcon icon="gem" className="me-5" />
                Sa7a7LY App
              </h6>
              <p>
                A Grades-autoFiller which converts either a tabular sheet of
                grades or a bubble sheet to an excel file with corresponding
                input mapped to answers.
              </p>
            </MDBCol>

            <MDBCol md="2" lg="2" xl="2" className="mx-auto mb-4">
              <h6 className="text-uppercase fw-bold mb-4">GitHubs</h6>
              <p>
                <a href="https://github.com/ZiadSheriif" className="text-reset">
                  ZiadSheriif
                </a>
              </p>
              <p>
                <a
                  href="https://github.com/Abd-ELrahmanHamza"
                  className="text-reset"
                >
                  Abd-ELrahmanHamza
                </a>
              </p>
              <p>
                <a
                  href="https://github.com/AbdelrahmanHamdyy"
                  className="text-reset"
                >
                  AbdelrahmanHamdyy
                </a>
              </p>
              <p>
                <a
                  href="https://github.com/Ahmedsabry11"
                  className="text-reset"
                >
                  Ahmedsabry11
                </a>
              </p>
            </MDBCol>

            <MDBCol md="3" lg="2" xl="2" className="mx-auto mb-4">
              <h6 className="text-uppercase fw-bold mb-4">Useful links</h6>
              <p>
                <a href="#!" className="text-reset">
                  About
                </a>
              </p>
              <p>
                <a href="#!" className="text-reset">
                  Settings
                </a>
              </p>
              <p>
                <a href="#!" className="text-reset">
                  Documentation
                </a>
              </p>
              <p>
                <a href="#!" className="text-reset">
                  Help
                </a>
              </p>
            </MDBCol>

            <MDBCol md="4" lg="3" xl="3" className="mx-auto mb-4">
              <h6 className="text-uppercase fw-bold mb-4">Contact</h6>
              <p>
                <MDBIcon icon="home" className="me-0" />
                Cairo, Egypt
              </p>
              <p>
                <MDBIcon icon="envelope" className="me-0" />
                Sa7a7LY@gmail.com
              </p>
              <p>
                <MDBIcon icon="phone" className="me-0" />
                +00201146188908
              </p>
              <p>
                <MDBIcon icon="print" className="me-0" />
                +01 234 567 89
              </p>
            </MDBCol>
          </MDBRow>
        </MDBContainer>
      </section>

      <div
        className="text-center p-4"
        style={{ backgroundColor: "rgba(0, 0, 0, 0.05)" }}
      >
        © 2023 Copyright:{" "}
        <a className="text-reset fw-bold" href="https://Sa7a7LY.com/">
          Sa7a7LY.com
        </a>
      </div>
    </MDBFooter>
  );
}

export default Footer;
