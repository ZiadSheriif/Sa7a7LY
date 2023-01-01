// Import styled
import styled from "styled-components";

// Import bootstrap components
import { Button } from "react-bootstrap";

export const DragAndDropFrame = styled.div`
  display: flex;
  align-items: center;
  /* If there is uploaded file make flex start */
  justify-content: ${({ containFiles }) =>
    containFiles ? "flex-start" : "center"};
  padding: 12px;
  /* If there is uploaded file make height fits content */
  min-height: ${({ containFiles }) => (containFiles ? "fit-content" : "280px")};
  border-radius: 4px;
  text-align: center;
  border: 1px dashed ${({ theme }) => theme.lineColor.primary};
  color: ${({ theme }) => theme.color.secondary};
`;

export const DragDropParagraph = styled.p`
  color: ${({ theme }) => theme.color.link};
  font-size: 1rem;
`;

export const UploadButton = styled(Button)`
  background-color: ${({ theme }) => theme.background.primary};
  color: ${({ theme }) => theme.color.secondary};
  border-color: ${({ theme }) => theme.color.secondary};
  font-weight: bold;
  border-radius: 9999px;
  margin-left: 10px;
  padding: 3px 13px;
  &:hover {
    border-color: ${({ theme }) => theme.color.secondary};
    color: ${({ theme }) => theme.color.secondary};
    background-color: ${({ theme }) => theme.background.muted};
  }
`;
