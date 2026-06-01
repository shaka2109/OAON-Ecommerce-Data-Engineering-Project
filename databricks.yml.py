# Databricks notebook source
bundle:
  name: oaon-ecommerce

include:
  - resources/*.yml

targets:
  dev:
    default: true
    workspace:
      host: https://adb-xxxxxxxxxxxxxxxx.x.azuredatabricks.net
