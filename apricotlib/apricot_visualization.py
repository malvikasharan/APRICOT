#!/usr/bin/env python 

import argparse
from collections import defaultdict
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

__description__ = "Creates visualization files for the APRICOT analysis data"
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("annotation_scoring_data")
    parser.add_argument("additional_annotation")
    parser.add_argument("outpath")
    args = parser.parse_args()

    biojs_viz_of_apricot_analysis = BiojsVizOfApricotAnalysis(
        args.annotation_scoring_data,
        args.additional_annotation, args.outpath)
    biojs_viz_of_apricot_analysis.parse_annotation_scoring()
    biojs_viz_of_apricot_analysis.viz_domain_highlights()
    biojs_viz_of_apricot_analysis.viz_annotation_scoring()
    biojs_viz_of_apricot_analysis.viz_secondary_structure()
    biojs_viz_of_apricot_analysis.sec_str_script()
    biojs_viz_of_apricot_analysis.viz_subcellular_localization()
    biojs_viz_of_apricot_analysis.viz_homologous_pdb_msa()


class BiojsVizOfApricotAnalysis(object):
    def __init__(self, annotation_scoring_data,
                 additional_annotation,
                 outpath):
        self._annotation_scoring_data = annotation_scoring_data
        self._additional_annotation = additional_annotation
        self._outpath = outpath
        self._sec_str = self._outpath+'/secondary_structure'
        self._dom_highlight = self._outpath+'/domain_highlighting'
        self._pdb_msa = self._outpath+'/homologous_pdb_msa'
        self._overview = self._outpath+'/overview_and_statistics'
        self._localize = self._outpath+'/subcellular_localization'
        self._annotation_data = []
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
        self.parse_annotation_scoring()
        self.viz_domain_highlights()
        self.domain_highlight_script()
        self.viz_annotation_scoring()
        self.viz_secondary_structure()
        self.sec_str_script()
        self.viz_subcellular_localization()
        self.viz_homologous_pdb_msa()
        
    def parse_annotation_scoring(self):
        with open(self._annotation_scoring_data, 'r') as in_fh:
            for entry in in_fh:
                self._annotation_data.append(entry.strip())
        return self._annotation_data
    
    def viz_domain_highlights(self):
        for entry in self._annotation_data:
            if not entry.startswith('Entry'):
                anno_score = AnnotationScoringColumns(
                    entry.strip().split('\t'))
                prot_name = anno_score.entry_name
                prot_end = int(anno_score.length)-1
                prot_key = '\n'.join(
                    ["\tstart: 0,", "\tend: %s,"
                     % prot_end, '\tname: "%s",' % prot_name,
                     '\thref: "http://www.uniprot.org/uniprot/%s"'
                     % anno_score.uid])
                self._uid_key_dict[anno_score.uid] = prot_key
                self._location_dict[
                    anno_score.uid][anno_score.domain_id].append(
                        '\t{start: %s, end: %s}' % (
                            anno_score.start, anno_score.stop))
                self._dom_annotation[
                    anno_score.domain_id] = anno_score.full_name
                src = anno_score.resource
                if src == 'CDD':
                    self._dom_rank.setdefault(
                        anno_score.uid+':CDD', []).append(
                        anno_score.domain_id)
                    self._highlight_dict.setdefault(
                        prot_key, []).append('\n'.join(
                            ['\t\tstart: %s,' % anno_score.start,
                             '\t\tend: %s,' % anno_score.stop,
                             '\t\tdomain: {', '\t\t\tname: "%s",'
                             % anno_score.domain_id,
                             '\t\t\tid: %s,' % len(
                                 self._dom_rank[anno_score.uid+':CDD']),
                             '\t\t\tdescription: "%s"},' %
                             anno_score.short_name,
                             '\t\tsource: {', '\t\t\tname: "CDD",',
                             '\t\t\thref: null,', '\t\t\tid: 1}']))
                else:
                    self._dom_rank.setdefault(
                        anno_score.uid+':IPR', []).append(
                        anno_score.domain_id)
                    self._highlight_dict.setdefault(
                        prot_key, []).append('\n'.join(
                            ['start: %s,' % anno_score.start,
                             'end: %s,' % anno_score.stop,
                             'domain: {', '\t\tname: "%s",' %
                             anno_score.domain_id,
                             '\t\tid: %s,' % len(
                                 self._dom_rank[anno_score.uid+':IPR']),
                             '\t\tdescription: "%s"},' % anno_score.short_name,
                             'source: {', '\t\tname: "InterPro",',
                             '\t\thref: null,', '\t\tid: 2}']))
        return(self._highlight_dict, self._uid_key_dict, self._location_dict, self._dom_annotation)
                
    def domain_highlight_script(self):
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
        '''annotation scoring stats, distribution, ref vs query sequence sec str, table'''
        
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
                sys.exit()
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
                            sys.exit()
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
        return self._fasta_dict, self._secstr_dict
                
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
            sys.exit()
        
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
        
if __name__ == '__main__':
    main()
