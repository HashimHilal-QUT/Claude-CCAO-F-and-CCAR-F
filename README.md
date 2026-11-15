# Claude-CCAO-F-and-CCAR-F
Exam Preparation Questions for Claude Certified Associate - Foundations (CCAO-F) and Claude Certified Architect – Foundations (CCAR-F)

## Live website

https://ccaoccaf.z8.web.core.windows.net/

## Exam preparation site

The static site in [`site/`](site/) provides searchable study cards and timed practice quizzes for both question banks. The question dataset is generated from the JSONL sources:

```bash
python3 site/build_questions.py
```

The generated site can be opened locally with any static file server, for example `python3 -m http.server --directory site`.

The **CCAR-F Training Hub** adds five chapter guides, 35 podcast episodes, the 27-page Architect's Playbook PDF, and a 120-question training quiz. The catalog is generated with `python3 site/build_training.py` when the private `CCAR-F_Training/` source folder is available. The large MP3, PDF, and Markdown assets are hosted directly in Azure under the `training/` prefix rather than stored in GitHub.

### Azure deployment

The GitHub Actions workflow in [`.github/workflows/deploy-site.yml`](.github/workflows/deploy-site.yml) rebuilds the dataset and publishes `site/` to the Azure Blob Storage `$web` container on pushes to `main` or by manual dispatch. Store this one GitHub Actions secret:

| Secret | Value |
| --- | --- |
| `AZURE_STORAGE_CONNECTION_STRING` | The complete Azure Storage connection string for the `ccaoccaf` account |

The storage account's static website endpoint is typically `https://ccaoccaf.z13.web.core.windows.net/`. The blob endpoint form, which is useful for verification, is `https://ccaoccaf.blob.core.windows.net/$web/index.html`.
