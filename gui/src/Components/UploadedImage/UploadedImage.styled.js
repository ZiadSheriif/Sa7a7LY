// Import styled
import styled from "styled-components";

// Import bootstrap components
import { Image } from "react-bootstrap";

export const StyledUploadedImage = styled(Image)`
  width: 100px;
  min-width: 100px;
  height: 100px;
  object-fit: cover;
  display: inline-block;
  border-radius: 4px;
  border: ${({ selected }) =>
    selected ? `2px solid ${({ theme }) => theme.color.muted}` : "none"};
  opacity: ${({ selected }) => (selected ? "1" : "0.5")};
  background-color: ${({ theme }) => theme.background.primary};
  &:hover {
    opacity: 1;
  }
`;

export const Thumb = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  &:hover {
    cursor: grab;
  }
`;

export const ThumbInner = styled.div`
  display: flex;
  min-width: 0;
  overflow: hidden;
  margin: 0 12px 12px 0;
  position: relative;
  &:hover {
    button {
      display: inline-flex;
    }
  }
`;

export const DeleteButton = styled.button`
  height: 22px;
  width: 22px;
  border-radius: 50%;
  display: none;
  align-items: center;
  justify-content: center;
  background-color: ${({ theme }) => theme.color.primary};
  color: ${({ theme }) => theme.background.primary};
  position: absolute;
  right: 8px;
  top: 8px;
  padding: 4px;
`;
