# HR Job Hierarchy – Structure Reports Enhancements (Odoo 18)

Extends `hr_job_hierarchy` by inheritance (the base module is untouched).

## Functional Structure By Sector (the former "Department Structure by Sector")
- Menu: Employees > Reporting > **Structure Reports** > Functional Structure By Sector
- Header/title "Functional Structure"; headcount removed from the cards (web + PDF)
- Cards coloured from the department's `hierarchy_level`: 0-2 -> N-1, 3 -> N-2, 4 -> N-3, 5+ -> N-4
- Overlap / connector fixes, +30px cards, logo + company name header,
  Deputy CEO shown on the committees side in its own colour
- Department form: `Hierarchy Level` is editable

## Positional Structure By Sector (new)
- Menu: Employees > Reporting > Structure Reports > Positional Structure By Sector
- Wizard: pick a **Department** (all its jobs + sub-departments' jobs) or a **Job Position**
  (that job and everyone reporting to it, down to the lowest position), ordered by *Reports To*
- Route: `/positional_structure_report?department_id=…` or `?job_id=…`
- New field **Level** (N-1..N-4) on Job Positions (form, below *Reports To*); card colours follow it.
  Jobs without a Level use the N-4 colour.

## Install
1. Copy the folder to your addons path, restart Odoo, Apps > Update Apps List, install.
2. The install first restores the report views of `hr_job_hierarchy` to their file version
   (manual developer-mode edits of those views are replaced by this module's inheritance).
3. Hard refresh the report (Ctrl+F5).

Tuning: card width = `--dsr-grow` in `static/src/css/dsr_report_enhance.css`; logo =
`static/src/img/dsr_logo.png`; company name = Settings > Companies.

## Level N-CEO-Office
Level value for CEO-office jobs (jobs flagged *CEO Office* get it automatically in the report).
Gray card, white text, drawn **beside** its Chief (its *Reports To* job) instead of below it;
anything reporting to a CEO-office job follows it into that side chain.
