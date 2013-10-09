import csv
import scipy.stats

with open('recovery-dump-normalized', 'r') as f:
  reader = csv.DictReader(f)
  recovery_journal_dataset = list(reader)

with open('counter-dump-normalized', 'r') as f:
  reader = csv.DictReader(f)
  qs_counters_dataset = list(reader)

print 'alcohol'
print '=' * 10
A = map(lambda row: float(row['alcohol']), recovery_journal_dataset[:31])
print 'avg(A) = %.2f' % (sum(A) / len(A))
B = map(lambda row: float(row['alcohol']), qs_counters_dataset[:31])
print 'avg(B) = %.2f' % (sum(B) / len(B))
print '(t, p) = (%.4f, %.4f)' % scipy.stats.ttest_rel(A, B)
print

print 'sweets'
print '=' * 10
A = map(lambda row: float(row['sweets']), recovery_journal_dataset[:31])
print 'avg(A) = %.2f' % (sum(A) / len(A))
B = map(lambda row: float(row['sweets']), qs_counters_dataset[:31])
print 'avg(B) = %.2f' % (sum(B) / len(B))
print '(t, p) = (%.4f, %.4f)' % scipy.stats.ttest_rel(A, B)
