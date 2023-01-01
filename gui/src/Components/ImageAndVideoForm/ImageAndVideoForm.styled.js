// Import styled
import styled from "styled-components";

// Import bootstrap components
import { Button } from "react-bootstrap";

export const StyledImageAndVideoFrom = styled.div`
  padding: 20px;

  .form-control:focus {
    box-shadow: none;
    border-color: ${({ theme }) => theme.color.primary};
  }

  .form-control {
    border-color: ${({ theme }) => theme.lineColor.primary};
    resize: none;
    background-color: ${({ theme }) => theme.background.primary};
    caret-color: ${({ theme }) => theme.color.primary};
  }

  .title-input {
    height: auto;
    padding-right: 50px;
    overflow: hidden;
    color: ${({ theme }) => theme.color.primary};
  }

  .title-group {
    display: flex;
    align-items: center;
    position: relative;
    span {
      position: absolute;
      right: 10px;
      font-size: 12px;
      color: ${({ theme }) => theme.color.muted};
      font-weight: 600;
    }
  }
`;

export const SubmitButtons = styled.div`
  display: flex;
  align-items: center;
  justify-content: flex-end;
  border-top: 1px solid ${({ theme }) => theme.lineColor.primary};
  padding: 20px 0;
`;

export const CancelButton = styled(Button)`
  margin-right: 10px;
  color: ${({ theme }) => theme.color.secondary};
  border-color: ${({ theme }) => theme.color.secondary};
  background-color: ${({ theme }) => theme.background.primary};

  border-radius: 9999px;
  font-weight: bold;
  padding: 4px 16px;
  &:hover {
    color: ${({ theme }) => theme.color.secondary};
    border-color: ${({ theme }) => theme.color.muted};
    background-color: ${({ theme }) => theme.button.hoverLight};
  }
`;

export const PostButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  color: ${({ theme, disabled }) =>
    disabled ? theme.background.muted : theme.background.primary};
  background-color: ${({ theme, disabled }) =>
    disabled ? theme.color.muted : theme.color.secondary};
  border-color: ${({ theme }) => theme.color.secondary};
  border-radius: 9999px;
  font-weight: bold;
  padding: 4px 16px;
  border: none;
  &:hover {
    color: ${({ theme, disabled }) =>
      disabled ? theme.background.muted : theme.background.primary};
    border-color: ${({ theme }) => theme.color.secondary};
    background-color: ${({ theme, disabled }) =>
      disabled ? theme.color.muted : theme.button.hoverBlue};
  }
`;
