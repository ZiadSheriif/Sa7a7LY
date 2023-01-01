// Import styled
import styled from "styled-components";

export const ThumbsContainer = styled.aside`
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  margin-top: 16;
  overflow: auto;
`;

export const UploadIcon = styled.button`
  width: 100px;
  min-width: 100px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 12px 12px 0;
  display: inline-block;
  color: ${({ theme }) => theme.color.muted};
  border-radius: 4px;
  background-color: ${({ theme }) => theme.background.primary};
  border: 1px dashed ${({ theme }) => theme.lineColor.primary};
`;
