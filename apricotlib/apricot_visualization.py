#!/usr/bin/env python
# Description = Visualizes different output data from APRICOT analysis

from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

try:
    import subprocess
except ImportError:
    print('Python package subprocess is missing. Please install/update.\n')
    sys.exit(0)
try:
    import shutil
except ImportError:
    print('Python package shutil is missing. Please install/update.\n')
    sys.exit(0)


class VizApricotAnalysis(object):
    def __init__(self, annotation_scoring_data,
                 domain_file,
                 additional_annotation,
                 outpath):
        self._annotation_scoring_data = annotation_scoring_data
        self._domain_file = domain_file
        self._additional_annotation = additional_annotation
        self._outpath = outpath
        self._sec_str = self._outpath+'/secondary_structure'
        self._dom_highlight = self._outpath+'/domain_highlighting'
        self._pdb_msa = self._outpath+'/homologous_pdb_msa'
        self._overview = self._outpath+'/overview_and_statistics'
        self._localize = self._outpath+'/subcellular_localization'
        self._annotation_data = []
        self._filter_viz_dict = {}
        self._highlight_dict = {}
        self._uid_key_dict = {}
        self._dom_rank = {}
        self._fasta_dict = {}
        self._secstr_dict = {}
        self._dom_annotation = {}
        self._location_dict = defaultdict(lambda: defaultdict(lambda: []))
        self._sec_str_color = {'H': '#FF6666', 'E': '#33CCCC', 'C': '#FFFFCC'}
        self._localization_dict = defaultdict(
            lambda: defaultdict(lambda: float))
        self._color_list = (
            "Blue", "Green", "Teal", "Lime", "SeaGreen", "MediumTurquoise",
            "Pink", "DarkOliveGreen", "Indigo", "Orange", "SlateBlue",
            "LawnGreen", "Brown", "LightSkyBlue", "LightGreen", "DarkOrchid",
            "GoldenRod", "MidnightBlue", "LightPink", "Gold")

    def viz_all_the_visualization_files(self):
        self.viz_domain_data()
        self.domain_highlight()
        self.viz_annotation_scoring()
        self.viz_secondary_structure()
        self.viz_subcellular_localization()
        self.viz_homologous_pdb_msa()
    
    def viz_domain_data(self):
        with open(self._domain_file, 'r') as in_fh:
            for entry in in_fh:
                if not entry.startswith('Entry'):
                    domain_info = DomainDataColumns(
                        entry.strip().split('\t'))
                    prot_name = domain_info.entry_name
                    prot_end = int(domain_info.length)-1
                    prot_key = '\n'.join(
                        ["\tstart: 0,", "\tend: %s,"
                         % prot_end, '\tname: "%s",' % prot_name,
                         '\thref: "http://www.uniprot.org/uniprot/%s"'
                         % domain_info.uid])
                    self._uid_key_dict[domain_info.uid] = prot_key
                    self._location_dict[
                        domain_info.uid][domain_info.domain_id].append(
                            '\t{start: %s, end: %s}' % (
                                domain_info.start, domain_info.stop))
                    self._dom_annotation[
                        domain_info.domain_id] = domain_info.full_name
                    src = domain_info.resource
                    if src == 'CDD':
                        self._dom_rank.setdefault(
                            domain_info.uid+':CDD', []).append(
                            domain_info.domain_id)
                        self._highlight_dict.setdefault(
                            prot_key, []).append('\n'.join(
                                ['\t\tstart: %s,' % domain_info.start,
                                 '\t\tend: %s,' % domain_info.stop,
                                 '\t\tdomain: {', '\t\t\tname: "%s",'
                                 % domain_info.domain_id,
                                 '\t\t\tid: %s,' % len(
                                     self._dom_rank[domain_info.uid+':CDD']),
                                 '\t\t\tdescription: "%s"},' %
                                 domain_info.short_name,
                                 '\t\tsource: {', '\t\t\tname: "CDD",',
                                 '\t\t\thref: null,', '\t\t\tid: 1}']))
                    else:
                        self._dom_rank.setdefault(
                            domain_info.uid+':IPR', []).append(
                            domain_info.domain_id)
                        self._highlight_dict.setdefault(
                            prot_key, []).append('\n'.join(
                                ['start: %s,' % domain_info.start,
                                 'end: %s,' % domain_info.stop,
                                 'domain: {', '\t\tname: "%s",' %
                                 domain_info.domain_id,
                                 '\t\tid: %s,' % len(
                                     self._dom_rank[domain_info.uid+':IPR']),
                                 '\t\tdescription: "%s"},' % domain_info.short_name,
                                 'source: {', '\t\tname: "InterPro",',
                                 '\t\thref: null,', '\t\tid: 2}']))
            return self._uid_key_dict, self._location_dict, self._dom_annotation, self._dom_highlight, self._highlight_dict

    def domain_highlight(self):
        for uid in self._uid_key_dict.keys():
            header = '\n'.join(['<meta charset="UTF-8">'
            '<link type="text/css" rel="stylesheet" href="http://parce.li/bundle/biojs-vis-protein-viewer@0.1.4">',
            '<script src="https://wzrd.in/bundle/biojs-vis-protein-viewer@0.1.4"></script>',
            '<div id="j-main">', '</div>', '<script>',
            'var ProteinViewer = require("biojs-vis-protein-viewer");'])
            body = '\n'.join(['var highlightData = [', '\t{',
                '\n\t},\n\t{\n'.join(self._highlight_dict[
                    self._uid_key_dict[uid]]), '\t}', '];'])
            panel = '\n'.join(['var highlightLocusData = {',
                               self._uid_key_dict[uid], '};'])
            footer = '\n'.join([
                'var pv = new ProteinViewer({',
                '\tel: document.getElementById("j-main"),',
                '\tdata: highlightData,',
                '\tlocusData: highlightLocusData', '});',
                'pv.render();', '</script>'])
            with open(self._dom_highlight+'/%s.html' % uid, 'w') as out_fh:
                out_fh.write('\n'.join([header, body, panel, footer]))
                
    def viz_annotation_scoring(self):
        if os.path.exists(self._annotation_scoring_data):
            with open(self._annotation_scoring_data, 'r') as in_fh:
                for entry in in_fh:
                    if not entry.startswith('Entry'):
                        self._filter_viz_dict.setdefault('filter1_list', []).append(
                            float(entry.strip().split('\t')[-5]))
                        self._filter_viz_dict.setdefault('filter2_list', []).append(
                            float(entry.strip().split('\t')[-4]))
                        self._filter_viz_dict.setdefault('filter3_list', []).append(
                            float(entry.strip().split('\t')[-3]))
                        self._filter_viz_dict.setdefault('filter4_list', []).append(
                            float(entry.strip().split('\t')[-2]))
                        self._filter_viz_dict.setdefault('bayscore_list', []).append(
                            float(entry.strip().split('\t')[-1]))
                try:
                    label_list = range(0, len(self._filter_viz_dict['bayscore_list']))
                    plt.plot(sorted(self._filter_viz_dict['filter1_list']), 'ro', label='Filter-1 Score')
                    plt.plot(sorted(self._filter_viz_dict['filter2_list']), 'ys', label='Filter-2 Score')
                    plt.plot(sorted(self._filter_viz_dict['filter3_list']), 'g8', label='Filter-3 Score')
                    plt.plot(sorted(self._filter_viz_dict['filter4_list']), 'mp', label='Filter-4 Score')
                    plt.plot(sorted(self._filter_viz_dict['bayscore_list']), 'b^', label='Bayesian Score')
                    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                       ncol=3, mode="expand", borderaxespad=0.)
                    plt.xticks(label_list)
                    plt.xlabel('Annotation scores of selected proteins')
                    plt.ylabel('Filter/Bayesian score')
                    plt.savefig(os.path.join(self._overview, 'viz_annotation_scoring.png'))
                except KeyError:
                    print("!!! The annotation scoring file seems to be empty."
                          " Please reanalyse annotation score using the subcommand 'annoscore' !!!")
        else:
            print('The data for annotation scores do not exist,'
                  'please calculate the annotation score using the subcommand'
                  '"annoscore", the flag "-nd" can be used to specify the absolute path for needle.')
                
    def viz_secondary_structure(self):
        for uid in self._uid_key_dict.keys():
            if uid+'.horiz' in os.listdir(
            self._additional_annotation+'/protein_secondary_structure/'):
                files = uid+'.horiz'
            elif uid+'.plain' in os.listdir(
                self._additional_annotation+'/protein_secondary_structure/'):
                files = uid+'.plain'
                print("\nRaptorX secondary structure files are unavailable.")
                print("Visualizing secondary structure using literature based analysis.\n")
            else:
                print("\nRaptorX/literature-based secondary structure files are unavailable.")
                print("Exiting the current analysis.")
                print("Please re-run the secondary structure prediction by RaptorX\n")
                return
            secstr_list = []
            uid_secstr_dict = {}
            sec_data_sites = []
            with open(self._additional_annotation+
                '/protein_secondary_structure/'+files, 'r') as in_fh:
                for entry in in_fh:
                    if 'AA: ' in entry:
                        self._fasta_dict.setdefault(uid,
                        []).append(entry.strip().split('AA: ')[1])
                    if 'Pred: ' in entry:
                        try:
                            secstr_list.append(entry.strip().split('Pred: ')[1])
                        except IndexError:
                            print("\nRaptorX output file is incomplete. Exiting the current analysis.")
                            print("Please re-run the secondary structure prediction by RaptorX\n")
                            return
            for i, pred_data in enumerate(''.join(secstr_list)):
                    uid_secstr_dict[i] = pred_data
            for j in range(len(uid_secstr_dict)-1):
                if j == 0:
                    sec_data_sites.append(j)
                if not uid_secstr_dict[j] == uid_secstr_dict[j+1]:
                    sec_data_sites.append(j+1)
                    self._secstr_dict.setdefault(uid, []).append(
                        'mySequence.addHighlight({start:%s, end:%s, color:"Black", background:"%s"});'
                        %(int(sec_data_sites[-2])+1, int(j)+1,
                          self._sec_str_color[uid_secstr_dict[j]]))
            self._secstr_dict.setdefault(uid, []).append(
                'mySequence.addHighlight({start:%s, end:%s, color:"Black", background:"%s"});'
                %(int(sec_data_sites[-1])+1, int(list(uid_secstr_dict.keys())[-1])+1,
                  self._sec_str_color[uid_secstr_dict[j]]))
        self.sec_str_script()
                
    def sec_str_script(self):
        for uid in self._fasta_dict.keys():
            header = '\n'.join(['<meta charset="UTF-8">',
            '<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>',
            '<script src="https://wzrd.in/bundle/biojs-vis-sequence@0.1.7"></script>',
            '<script src="https://wzrd.in/bundle/biojs-io-fasta@latest"></script>',
            '<div id="snippetDiv"></div>', '<script>',
            'var yourDiv = document.getElementById("snippetDiv");',
            'var Seq = require("biojs-vis-sequence");'])
            footer = '\n'.join([
            'mySequence.on("all",function(name,data){var obj = {name: name, data: data};if(inIframe()){ parent.postMessage(obj, "*") }})',
            'mySequence.onAll(function(name,data){',
            'console.log(arguments);', '});', '};',
            'function inIframe(){try{return window.self!==window.top}catch(e){return true}}', 
            '</script>'])
            body1 = '\n'.join(['var theSequence = "%s";' %
            ''.join(self._fasta_dict[uid]), 'yourDiv.textContent = "";',
            'window.onload = function() {', 'var mySequence = new Seq({',
            '\tsequence : theSequence,', '\ttarget : yourDiv.id,',
            '\tformat : "CODATA",', '\tformatOptions : {',
            '\ttitle:false,', '\tfooter:false', '\t},', '\tid : "%s"' % uid, '});'])
            body2 = '\n'.join(self._secstr_dict[uid])
            dom_list = sorted(list(self._location_dict[uid].keys()))
            annotation_list = []
            for dom_id in dom_list:
                dom_idx = dom_list.index(dom_id)
                annotation_list.append('\n'.join([
                    'mySequence.addAnnotation({', 'name:"Domain-%s",' % str(int(dom_idx)+1),
                    'html:"<br>%s<br>%s</b>",' % (dom_id,
                    self._dom_annotation[dom_id]), 'color:"%s",' % self._color_list[dom_idx],
                    'regions: [', ',\n'.join(self._location_dict[uid][dom_id]), ']});']))
            with open(self._sec_str+'/'+uid+'.html', 'w') as out_fh:
                out_fh.write('\n'.join([header, body1, '\n'.join(annotation_list),
                                        body2, footer]))
        
    def viz_subcellular_localization(self):
        ''''''
        if 'psortb_data_summary.csv' in os.listdir(
            self._additional_annotation+'/protein_localization'):
            total_loc = set()
            with open(
            self._additional_annotation+'/protein_localization/psortb_data_summary.csv',
            'r') as in_fh:
                for entry in in_fh:
                    if not 'Localization' in entry:
                        protein = entry.strip().split('\t')[0]
                        localization = entry.strip().split('\t')[1]
                        if not localization.lower() == 'unknown':
                            score = float(entry.strip().split('\t')[2])
                            self._localization_dict[protein][localization] = score
                            total_loc.add(localization)
            with open(self._localize+'/localization_table.csv', 'w') as out_fh:
                out_fh.write('Proteins\t%s\n' % '\t'.join(sorted(list(total_loc))))
                for each_prot in self._localization_dict.keys():
                    for localization in self._localization_dict[each_prot]:
                        entry_list = list('0'*len(total_loc))
                        loc_idx = sorted(list(total_loc)).index(localization)
                        entry_list[loc_idx] = self._localization_dict[each_prot][localization]
                        out_fh.write("%s\t%s\n" % (each_prot, '\t'.join(map(str, entry_list))))
            self._create_localization_heatmap()
        else:
            print("\nPsortB-based localization prediction files are unavailable.")
            print("Exiting the current analysis.")
            print("Please re-run the localization prediction by PsortB\n")
            return
        
    def _create_localization_heatmap(self):
        ''''''
        plot_file = self._localize+'/localization_heatmap.pdf'
        infile = self._localize+'/localization_table.csv'
        with open(self._localize+'/localization_heatmap.R', 'w') as r_fh:
            r_fh.write('\n'.join(['library(gplots)', 'library(RColorBrewer)', 'display.brewer.all()',
        'data <- read.csv("%s", header=T, sep = "\\t")' % infile,
        'rnames <- data[,1]',  'data_matrix <- data.matrix(data[,2:ncol(data)])',
        'data_matrix[is.na(data_matrix)] <- 0', 'data_matrix[is.nan(data_matrix)] <- 0',
        'data_matrix[is.infinite(data_matrix)] <- max(data_matrix)',
        'rownames(data_matrix) <- rnames', 'pdf(file="%s")' % plot_file,
        'out_map <- heatmap.2(data_matrix, dendrogram = "none", Rowv = FALSE, \
        Colv = FALSE, col=brewer.pal(9,"YlGn"), margins=c(5,8), \
        cexCol=0.8, cexRow=0.8, key.title="PsortB Pred-value", key.xlab="", key.ylab="")',
        'dev.off()']))
        subprocess.Popen(['Rscript %s/localization_heatmap.R' %
                          self._localize], shell=True).wait()
        
    def viz_homologous_pdb_msa(self):
        header = '\n'.join(['<meta charset="UTF-8">',
        '<link type="text/css" rel="stylesheet" href="http://parce.li/bundle/msa@0.4.8">',
        '<script src="https://wzrd.in/bundle/msa@0.4.8"></script>',
        '<script src="https://wzrd.in/bundle/biojs-io-fasta@latest"></script>',
        '<script src="https://wzrd.in/bundle/biojs-io-clustal@latest"></script>',
        '<script src="https://wzrd.in/bundle/biojs-io-gff@latest"></script>',
        '<script src="https://wzrd.in/bundle/xhr@latest"></script>',
        '<div id="snippetDiv"></div>', '<script>',
        'var rootDiv = document.getElementById("snippetDiv");',
        'var msa = require("msa");', 'var menuDiv = document.createElement("div");',
        'var msaDiv = document.createElement("div");',
        'rootDiv.appendChild(menuDiv);', 'rootDiv.appendChild(msaDiv);'])
        footer = '\n'.join(['opts.conf = {', '\tdropImport: true,',
        '\tmanualRendering: true', '};', 'opts.vis = {', '\tconserv: false,',
        '\toverviewbox: false,', '\tseqlogo: true,', '\tmetacell: true', '};',
        'opts.zoomer = {', '\tlabelIdLength: 20', '};', 'var m = msa(opts);',
        'gg = m;', 'm.u.file.importURL(url, function() {',
        '\tvar defMenu = new msa.menu.defaultmenu({', '\t\tel: menuDiv,',
        '\t\tmsa: m', '\t});', '\tdefMenu.render();', '\tm.render();', '});',
        'm.g.on("all",function(name,data){var obj = {name: name, data: data};if(inIframe()){ parent.postMessage(obj, "*") }})',
        'function inIframe(){try{return window.self!==window.top}catch(e){return true}}',
        '</script>'])
        body = '//EDIT PATH\n'.join([
        'var url = "https://github.com/malvikasharan/APRICOT/blob/master/Biojs_dependencies/data/biojs_msa_tab.clustal";'
        'var opts = {', '\tel: msaDiv', '};'])
        with open(self._pdb_msa+'/Biojs_pdb_msa_tab.html', 'w') as out_fh:
            out_fh.write('\n'.join([header, body, footer]))
            
        for files in os.listdir(self._additional_annotation+'/pdb_sequence_prediction/'):
            if '_top5.fasta' in files:
                shutil.copyfile(
                self._additional_annotation+'/pdb_sequence_prediction/'+files,
                self._pdb_msa+'/'+files)
                subprocess.Popen(['bin/reference_db_files/clustal/clustalw2 %s' %
                    self._pdb_msa+'/'+files], shell=True).wait()
                
        print("\nPlease open the BioJS MSA tab generated in Biojs_pdb_msa_tab.html.")
        print("Import MSA files (.aln) in the BioJS MSA tab to visualize the alignment.\n")

class AnnotationScoringColumns(object):
    '''Column information of annotation scoring file'''
    def __init__(self, row):
        self.uid = row[0]
        self.entry_name = row[1]
        self.prot_name = row[2]
        self.species = row[3]
        self.length = row[4]
        self.resource = row[5]
        self.resource_id = row[6]
        self.domain_id = row[7]
        self.short_name = row[8]
        self.full_name = row[9]
        self.domain_length = row[10]
        self.start = row[11]
        self.stop = row[12]
        self.ref_seq = row[13]
        self.q_seq = row[14]
        self.ref_ss = row[15]
        self.q_ss = row[16]
        self.mol_mass = row[17]
        self.iso_pt = row[18]
        self.solub = row[19]
        self.vdw = row[20]
        self.coverage = row[21]
        self.cov_by_dom = row[22]
        self.identity = row[23]
        self.iden_by_cov = row[24]
        self.similarity = row[25]
        self.sim_by_cov = row[26]
        self.gap = row[27]
        self.gap_by_cov = row[28]
        self.AA_RO = row[29]
        self.SS_RO = row[30]
        self.PC_RO = row[31]
        self.AAC_ED = row[32]
        self.PCC_ED = row[33]
        self.DPC_ED = row[34]
        self.TPC_ED = row[35]

class DomainDataColumns(object):
    '''Column information of domain annotation file'''
    def __init__(self, row):
        self.uid = row[0]
        self.entry_name = row[1]
        self.prot_name = row[2]
        self.species = row[3]
        self.length = row[4]
        self.gene_name = row[5]
        self.locus_tag = row[6]
        self.existance = row[7]
        self.go = row[8]
        self.embl_id = row[9]
        self.pdb_id = row[10]
        self.kegg_id = row[11]
        self.interpro_id = row[12]
        self.pfam_id = row[13]
        self.pubmed_id = row[14]
        self.resource = row[15]
        self.resource_id = row[16]
        self.domain_id = row[17]
        self.short_name = row[18]
        self.full_name = row[19]
        self.dom_kw = row[20]
        self.dom_go = row[21]
        self.members = row[22]
        self.dom_len = row[23]
        self.start = row[24]
        self.stop = row[25]
        self.evalue = row[26]
        self.bitscore = row[27]
        self.bits = row[28]
        self.cover_len = row[29]
        self.cov_prcnt = row[30]
        self.identity = row[31]
        self.iden_prcnt = row[32]
        self.similarity = row[33]
        self.sim_prcnt = row[34]
        self.gaps = row[35]
        self.gap_prcnt = row[36]
        self.filter_tag = row[37]
