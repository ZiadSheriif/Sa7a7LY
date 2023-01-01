// Import styled
import styled from "styled-components";

// Import bootstrap components
import { Form } from "react-bootstrap";

export const ImageContainer = styled.div`
  width: 50%;
  height: 324px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: ${({ theme }) => theme.background.lightMuted};
  margin: 12px 12px 12px 0;
`;

export const StyledPreviewImage = styled.div`
  display: flex;
  align-items: flex-start;
`;

export const Image = styled.img`
  object-fit: cover;
  display: inline-block;
  max-height: 100%;
  max-width: 100%;
`;

export const Video = styled.video`
  object-fit: cover;
  display: inline-block;
  max-height: 100%;
  max-width: 100%;
`;

export const LinkForm = styled(Form)`
  margin: 12px 12px 12px 0;
  width: 50%;
`;
