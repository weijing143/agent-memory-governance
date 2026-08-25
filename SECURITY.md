# Security Policy

## Scope

This repository contains a governance guide (`SKILL.md`) and reference materials for long-running AI agents. It does not execute memory operations, delete data, or access provider-side systems by itself.

## What This Project Does Not Do

- It does **not** automatically archive, delete, or rewrite any data.
- It does **not** erase provider-side memory, chat history, or hidden application state.
- It does **not** require API keys, credentials, or network access to function as a guide.

## Reporting Sensitive Information

If you discover that a contribution accidentally contains personal data, API keys, passwords, or other sensitive information, please report it immediately so it can be removed from both the repository and Git history.

To report:

1. Do **not** open a public issue.
2. Contact the maintainer via the email associated with the latest signed commits, or use GitHub's private vulnerability reporting feature if enabled.

## High-Impact Actions

The project explicitly discourages unattended automation for high-impact actions such as changing repository visibility, batch rewrites, permission changes, or mass moves. Any such actions require explicit user confirmation and a permitted executor.

## Version Support

Only the latest tagged release is actively maintained. Security-sensitive fixes will be released as a new patch version.
