# Databricks notebook source
resources:
  jobs:
    oaon_full_pipeline:

      name: OAON Full Pipeline

      tasks:

        - task_key: raw_load

          run_job_task:
            job_name: OAON Raw Load

        - task_key: bronze_load

          depends_on:
            - task_key: raw_load

          run_job_task:
            job_name: OAON Bronze Load

        - task_key: silver_load

          depends_on:
            - task_key: bronze_load

          run_job_task:
            job_name: OAON Silver Load
