# rules.awk — Convert ChordPro text-output to MarkdownV2
# Usage:
#    1) Run ChordPro to get a text version of song:
     chordpro song-file.cho --output song-file.txt
     2) Convert the txt-file to md-file:
#    awk -f rules.awk song-file.txt > song-file.md

# Title line → bold
/^-- Title: / {
  title = substr($0, 11)
  print "**" title "**"
  next
}

# Artist line → italic
/^-- Artist: / {
  artist = substr($0, 13)
  print "_Artist: " artist "_"
  next
}

# Verse block
/^-- Start of verse$/ {
  print "Куплет"
  print "```"
  next
}
/^-- End of verse$/ {
  print "```"
  next
}

# Chorus block
/^-- Start of chorus$/ {
  print "Припев"
  print "```"
  next
}
/^-- End of chorus$/ {
  print "```"
  next
}

# Bridge block
/^-- Start of bridge$/ {
  print "Бридж"
  print "```"
  next
}
/^-- End of bridge$/ {
  print "```"
  next
}

# All other lines — clean up leading/trailing dashes
{
  line = $0

  # Replace leading dashes (---...) with spaces of same length
  if (match(line, /^-+/)) {
    dashlen = RLENGTH
    line = substr(line, dashlen + 1)         # Remove leading dashes
    line = sprintf("%" dashlen "s", "") line # Prepend spaces
  }

  # Remove trailing dashes (---...)
  sub(/-+$/, "", line)

  print line
}