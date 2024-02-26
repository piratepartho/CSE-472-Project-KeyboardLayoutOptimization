#!/usr/bin/perl
use strict;
use warnings;
use Text::CSV;

binmode STDOUT, ':encoding(UTF-8)';

my $filename = 'wiki.csv';

my $csv = Text::CSV->new({ binary => 1, auto_diag => 1 });

open my $fh, '<:encoding(utf8)', $filename or die "Could not open '$filename' $!\n";

my $header = $csv->getline($fh);
$csv->column_names(@$header);

my %char_count = ();

while (my $row = $csv->getline_hr($fh)) {
    my $text = $row->{'text'};
    foreach my $char (split //, $text){
        my $codepoint = ord($char);
        
        if ($codepoint >= 0x0980 && $codepoint <= 0x09FF) {
            $char_count{$char}++;
        }
    }
}
foreach my $char (keys %char_count){
    print "$char $char_count{$char}\n"
}
my $len = scalar keys %char_count;
print "total len $len";

# Close the file handle
close $fh;

# my @bangla_chars = ();

# # Iterate through the Bangla Unicode range
# for (my $codepoint = 0x0980; $codepoint <= 0x09FF; $codepoint++) {
#     # Convert codepoint to actual character and add it to the array
#
#     push @bangla_chars, chr($codepoint);
# }

# # To demonstrate, print all Bangla characters (may not render correctly in all terminals)
# foreach my $char (@bangla_chars) {
#     print "$char ";
